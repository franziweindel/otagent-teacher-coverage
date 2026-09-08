#!/usr/bin/env python3
"""The tasks of OpenThoughts-Agent-SFT-10K, and the hash everything joins on.

SFT-10K's 10,000 rows are traces over 8,360 distinct tasks. Each row carries
the task's instruction.md inside the terminus-2 harness prompt; this module
strips the wrapper off, hashes what is left, and caches one row per task.

That hash is the join key as task ids cannot be used reliably: the
datasets renumber the same tasks and reuse ids across task-set generations, so
the same id often holds a different task. Tested 2026-08-18 between SFT-10K
and AgentTrove: 1,588 swesmith pairs shared a task id, and every one of them
held a different instruction.md. 

    python hash_sft10k_tasks.py --workers 8   # -> <cache>/sft_text.parquet, ~1 min
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem

SFT10K = "open-thoughts/OpenThoughts-Agent-SFT-10K"

#: Scratch, not backed up — everything here is rebuildable from the scripts.
DEFAULT_CACHE = Path("/data/cat/ws/frwe188h-otagent/tmp/agenttrove_cache")

#: The terminus-2 prompt is ``<harness boilerplate> Task Description:
#: <instruction.md> \n\nCurrent terminal state: <live screen>``. Cutting the
#: tail is not optional: it holds the sandbox container UUID, which is random
#: per rollout, so an uncut prompt does not even hash equal to itself.
_TASK_START = "Task Description:"
_TASK_END = "\n\nCurrent terminal state:"

#: 155 of the 8,360 prompts are retries prepending "## Hints from prior
#: attempts ... ## Task <the actual task>". Gated on the hints marker so a task
#: that legitimately contains "## Task" in its body is left alone.
_HINTS_MARK = "## Hints from prior attempts"
_TASK_HDR_RE = re.compile(r"##\s*Task\b")

_WS_RE = re.compile(r"\s+")
_COPY_RE = re.compile(r"_copy\d+$")                    # parallel-rollout dupes
_TRIAL_SUFFIX_RE = re.compile(r"__[A-Za-z0-9]{5,}$")   # trial_name random tail
_FAMILY_RE = re.compile(r"^(.*?)[-_]\d+$")             # <family>-<index>


def extract_task_text(message: object) -> object:
    """Strip the harness wrapper off a prompt, leaving the instruction.md text.

    Marker-driven and idempotent: text with no markers passes through
    unchanged, so bare instructions and wrapped prompts share one code path.
    """
    if not isinstance(message, str) or not message:
        return pd.NA
    s = message
    i = s.find(_TASK_START)
    if i >= 0:
        s = s[i + len(_TASK_START):]
    j = s.rfind(_TASK_END)
    if j >= 0:
        s = s[:j]
    k = s.find(_HINTS_MARK)
    if k >= 0:
        m = _TASK_HDR_RE.search(s, k + len(_HINTS_MARK))
        if m:
            s = s[m.end():]
    return s.strip()


def text_hash(text: object) -> object:
    """Whitespace-collapsed sha1 of an instruction text — the join key."""
    if not isinstance(text, str):
        return pd.NA
    s = _WS_RE.sub(" ", text).strip()
    if not s:
        return pd.NA
    return hashlib.sha1(s.encode("utf-8", "replace")).hexdigest()


def first_user_message(turns: object) -> object:
    """First user turn of a conversation, ShareGPT or OpenAI shaped."""
    conv = turns
    if isinstance(conv, str):
        try:
            conv = json.loads(conv)
        except Exception:
            return pd.NA
    if conv is None:
        return pd.NA
    try:
        items = list(conv)
    except TypeError:
        return pd.NA
    for turn in items:
        if not isinstance(turn, dict):
            continue
        role = turn.get("role") or turn.get("from") or ""
        if str(role).lower() in ("user", "human"):
            val = turn.get("content", turn.get("value"))
            return val if isinstance(val, str) else pd.NA
    return pd.NA


def add_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Derive ``base_id`` (``superuser-003114``) and ``family`` (``superuser``).

    ``task`` is null on ~14% of rows; recover it from ``trial_name``
    (``superuser-003114__c8ZdrpP``) when it is missing.
    """
    def from_trial(trial):
        if not isinstance(trial, str) or not trial:
            return pd.NA
        return _TRIAL_SUFFIX_RE.sub("", trial)

    def family(base_id):
        if not isinstance(base_id, str):
            return pd.NA
        m = _FAMILY_RE.match(base_id)
        return m.group(1) if m else base_id

    task = df["task"] if "task" in df.columns else pd.Series(pd.NA, index=df.index)
    trial = (df["trial_name"] if "trial_name" in df.columns
             else pd.Series(pd.NA, index=df.index))
    task_id = task.where(task.notna() & (task != ""), trial.map(from_trial))
    df["base_id"] = task_id.map(
        lambda t: _COPY_RE.sub("", t) if isinstance(t, str) and t else pd.NA)
    df["family"] = df["base_id"].map(family)
    return df


def shard_paths(repo: str) -> list[str]:
    files = sorted(HfFileSystem().glob(f"datasets/{repo}/**/*.parquet"))
    if not files:
        raise ValueError(f"no parquet shards found for {repo}")
    return files


def present(pf: pq.ParquetFile, cols: list[str]) -> list[str]:
    have = set(pf.schema_arrow.names)
    return [c for c in cols if c in have]


def _read_shard(path: str) -> list[pd.DataFrame]:
    """All task rows of one parquet shard (its own HfFileSystem: thread use)."""
    pf = pq.ParquetFile(HfFileSystem().open(path, "rb"))
    cols = present(pf, ["task", "trial_name", "conversations", "run_id"])
    frames = []
    for rg in range(pf.metadata.num_row_groups):
        df = add_id_columns(pf.read_row_group(rg, columns=cols).to_pandas())
        df["text"] = (df["conversations"].map(first_user_message)
                      .map(extract_task_text))
        if "run_id" not in df:
            df["run_id"] = pd.NA
        frames.append(df[["base_id", "family", "text", "run_id"]])
    return frames


def build_sft_text(out: Path, workers: int = 8) -> pd.DataFrame:
    """One row per SFT-10K task: ``base_id``, ``family``, ``text``, ``run_id``.

    ``run_id`` is the generation run the trajectory came from. SFT-10K's
    teacher is known, so a run_id seen here pins the teacher of any other repo
    that carries the same run_id (see ``teacher_coverage.resolve_bare_glm``).

    Shards are fetched ``workers`` at a time; the work is network-bound.
    """
    files = shard_paths(SFT10K)
    frames = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fi, shard in enumerate(pool.map(_read_shard, files)):
            frames.extend(shard)
            print(f"  [{fi + 1}/{len(files)}] {files[fi].split('/')[-1]}",
                  file=sys.stderr)
    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["base_id", "text"]).drop_duplicates("base_id")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    print(f"  -> {out}  ({len(df):,} task texts)", file=sys.stderr)
    return df


def load_tasks(cache: Path = DEFAULT_CACHE, workers: int = 8) -> pd.DataFrame:
    """Cached SFT-10K tasks with their join hash. Build it if missing."""
    out = cache / "sft_text.parquet"
    df = pd.read_parquet(out) if out.exists() else build_sft_text(out, workers)
    if "run_id" not in df.columns:            # cache from before run_id was kept
        df = build_sft_text(out, workers)
    col = "task_text" if "task_text" in df.columns else "text"
    df["hash"] = df[col].map(text_hash)
    return df


def hashes_path(cache: Path, repo: str) -> Path:
    """Where every instruction hash a repo holds is memoised.

    The SFT-10K match is derived from this by a local join, so asking a new
    question about the traces costs no refetch.
    """
    return (cache / "sweep" / "hashes"
            / (re.sub(r"[^A-Za-z0-9]+", "_", repo) + ".parquet"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    ap.add_argument("--workers", type=int, default=8,
                    help="shards fetched concurrently; the work is network-bound")
    args = ap.parse_args()
    df = load_tasks(args.cache, args.workers)
    print(f"{len(df):,} tasks, {df['hash'].nunique():,} distinct hashes")
    print(df.groupby("family")["base_id"].nunique().to_string())


if __name__ == "__main__":
    main()
