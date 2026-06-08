#!/usr/bin/env python3
"""Claude Code status line: model | context used/total (%) | session cost | duration.

Reads the status JSON from stdin (see Claude Code statusLine docs) and prints a
single colored line using the Dracula palette (24-bit truecolor, no icons).
"""

import json
import sys

# --- Dracula palette (24-bit truecolor) ---
RESET = "\033[0m"
CYAN = "\033[38;2;139;233;253m"  # #8be9fd
GREEN = "\033[38;2;80;250;123m"  # #50fa7b
YELLOW = "\033[38;2;241;250;140m"  # #f1fa8c
RED = "\033[38;2;255;85;85m"  # #ff5555
PINK = "\033[38;2;255;121;198m"  # #ff79c6
PURPLE = "\033[38;2;189;147;249m"  # #bd93f9
COMMENT = "\033[38;2;98;114;164m"  # #6272a4
SEP = f"{COMMENT} | {RESET}"

# --- Token-count formatting thresholds ---
THOUSAND = 1000
MILLION = 1_000_000

# --- Context-usage percentage thresholds for color coding ---
CTX_WARNING_PCT = 50
CTX_CRITICAL_PCT = 80


def color(text, c):
    return f"{c}{text}{RESET}"


def fmt_k(n):
    """Human-readable token count: 200000 -> '200k', 77516 -> '77.5k', 1000000 -> '1M'."""
    if n < THOUSAND:
        return str(n)
    if n >= MILLION:
        m = n / MILLION
        return f"{int(m)}M" if m == int(m) else f"{m:.1f}M"
    k = n / THOUSAND
    return f"{int(k)}k" if k == int(k) else f"{k:.1f}k"


def fmt_duration(ms):
    """Milliseconds -> 'Hh Mm' / 'Mm Ss' / 'Ss', trimming leading zero units."""
    total_s = ms // 1000
    h, rem = divmod(total_s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}

    model = (data.get("model") or {}).get("display_name") or "Claude"
    effort = (data.get("effort") or {}).get("level")
    model_segment = f"{model} {effort}" if effort else model

    cost = data.get("cost") or {}
    cost_usd = cost.get("total_cost_usd", 0) or 0
    dur_ms = cost.get("total_duration_ms", 0) or 0

    cw = data.get("context_window") or {}
    used = cw.get("total_input_tokens", 0) or 0
    limit = cw.get("context_window_size", 200_000) or 200_000
    pct = cw.get("used_percentage")
    if pct is None:
        pct = used * 100 / limit
    pct = int(pct)

    ctx_color = RED if pct >= CTX_CRITICAL_PCT else YELLOW if pct >= CTX_WARNING_PCT else GREEN

    segments = [
        color(model_segment, CYAN),
        color(f"{fmt_k(used)}/{fmt_k(limit)} ({pct}%)", ctx_color),
        color(f"${cost_usd:.2f}", PINK),
        color(fmt_duration(dur_ms), PURPLE),
    ]
    sys.stdout.write(SEP.join(segments))


if __name__ == "__main__":
    main()
