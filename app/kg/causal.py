
"""Simple causal heuristics for temporal-causal KG.

This module implements a simple, explainable causal scoring heuristic that is
safe for MVP and easily replaceable with causal-learn / DoWhy later.

Heuristic (configurable weights):
- temporal precedence score: does event A happen before B within a time window?
- co-occurrence score: how often A and B appear together in same episodes
- metadata_signal: e.g., explicit "because" markers in text (not reliable but helpful)

Returns a score in [0,1].
"""
from datetime import datetime, timedelta
import math

def parse_ts(ts):
    if ts is None:
        return None
    try:
        return datetime.fromisoformat(ts.replace('Z',''))
    except Exception:
        return None

def temporal_precedence_score(ts_src, ts_dst, window_seconds=3600*24*7):
    # If src happens before dst within window, higher score
    a = parse_ts(ts_src)
    b = parse_ts(ts_dst)
    if not a or not b:
        return 0.0
    if a >= b:
        return 0.0
    delta = (b - a).total_seconds()
    if delta > window_seconds:
        return 0.0
    # linear decay: 1.0 at delta=0, 0.0 at delta=window_seconds
    return max(0.0, 1.0 - (delta / window_seconds))

def cooccurrence_score(count_joint, count_a, count_b):
    # Jaccard-like score
    if count_a + count_b - count_joint <= 0:
        return 0.0
    return count_joint / (count_a + count_b - count_joint)

def causal_score(ts_src, ts_dst, count_joint=1, count_a=1, count_b=1, weights=(0.6,0.4)):
    tscore = temporal_precedence_score(ts_src, ts_dst)
    cscore = cooccurrence_score(count_joint, count_a, count_b)
    w1, w2 = weights
    return max(0.0, min(1.0, w1*tscore + w2*cscore))
