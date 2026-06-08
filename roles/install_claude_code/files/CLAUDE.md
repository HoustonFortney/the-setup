## Workflow

- For non-trivial tasks, propose a short plan and ask for approval before editing files or running mutating commands
- Trivial, read-only, or explicitly-requested actions don't need a plan or approval
- Surface blockers instead of guessing around them
- If anything is ambiguous, has multiple reasonable approaches, or you have
  doubts don't guess, ask

## Communication

- Explain why only when non-obvious or I'm likely to disagree
- Don't over-explain fundamentals

## Coding defaults

- Prefer `uv` for Python unless unavailable or the project uses something else
- Prefer `rg` over grep and `fd`/`fdfind` over find
- Comment only when it adds something not in the code, or explains a non-obvious choice
- For bugs: reproduce first then confirm the fix resolves it
- Never commit or push unless I explicitly ask
- Don't install system wide packages without asking

