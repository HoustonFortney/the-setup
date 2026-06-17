## Workflow

- For non-trivial tasks, propose a short plan and ask for approval before editing files or running mutating commands
- Trivial, read-only, or explicitly-requested actions don't need a plan or approval
- For bugs: reproduce first then confirm the fix resolves it

## Communication

- Surface blockers instead of guessing around them
- If anything is ambiguous, has multiple reasonable approaches, or you have doubts don't guess, ask
- Don't over-explain fundamentals

## Tools

- Prefer `uv` for Python unless unavailable or the project uses something else
- Don't install system wide packages without asking
- Never commit or push unless I explicitly ask

## Coding style

- Comment only when it adds something not in the code, or explains a non-obvious choice
- Favor simplicity and minimalism

