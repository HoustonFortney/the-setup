#!/usr/bin/env bash

set -uo pipefail

[ -n "${TMUX:-}" ] || exit 0

tmux display-message -d 3000 "🔔 Claude needs you" 2>/dev/null || true

exit 0
