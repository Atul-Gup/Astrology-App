# Astrology App: starter kit for Claude Code

This folder is a ready-to-use project folder for building the Vedic Career Timing Report app with Claude Code in a terminal on your laptop.

## What is in here
- `CLAUDE.md`: the file Claude Code reads at the start of every session. It holds the rules and project context.
- `docs/`: the build document, product spec, and decisions list.
- `tasks/`: milestone task lists. M0 (calculation service) is detailed; M1-M4 are outlined.
- `prompts/first-prompt.md`: the exact first message to give Claude Code.
- `data/golden/`: where your reference birth charts go (you create these; Claude Code cannot).
- `data/rules/`: where the astrologer's rule table goes.
- `services/calc/`: where the Python calculation service will live. It has its own `CLAUDE.md`.

## Setup (about 15 minutes)
1. Install Claude Code by following the official quickstart: https://code.claude.com/docs/en/quickstart . It needs a paid Claude plan; check the docs for current requirements.
2. Copy this folder to where you keep projects, open a terminal in it, and run `git init` then make a first commit. Keep it local if you prefer; GitHub is not required.
3. Start Claude Code in this folder with `claude`.
4. Paste the prompt from `prompts/first-prompt.md`.

## How to work with it
- Plan first. Use plan mode (`/plan`, or start with `claude --permission-mode plan`) so Claude proposes what it will do and waits for your approval.
- One task at a time, from `tasks/`. Ask for tests first, a commit at the end.
- Review diffs yourself. You do not need to read every line, but read the test results and the summary.
- When Claude asks about an astrological rule or convention, answer from your reviewer or reference software. Do not let it guess.
- Keep `CLAUDE.md` current. If Claude repeats a mistake, add a rule to that file.
- Run `/init` only if you want Claude to regenerate a CLAUDE.md; this kit already has one, and `/init` could overwrite what you have written.

## Your own tasks (Claude Code cannot do these)
1. Build the golden set: 40-50 birth charts with reference values from established software (see `data/golden/README.md`).
2. Choose and hire the astrologer reviewers (see `docs/` and the review plan in your Claude project).
3. Decide the conventions listed in `tasks/M0-calculation-service.md` once you can see the reference software's settings.
4. Set the test budget and the cost-per-paid-report ceiling before M3.

## Order of work
M0 calculation service and golden tests, M1 web funnel with fake payment, M2 payments and PDF, M3 admin, analytics, legal review and a small soft launch, M4 Android. Do not start M1 until M0 passes its golden tests.
