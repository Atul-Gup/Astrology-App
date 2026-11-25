# Astrology App: project guide for Claude Code

Read this file first in every session. Detailed requirements live in `docs/`.

## What this is
A paid Vedic Career Timing Report. Users enter birth details, verify by OTP, ask one career question for free, then pay (Rs 199-299 test) for a 12-month timing report as a PDF in English or Hindi. v1 is web first, Android (Capacitor wrapper) last. Solo founder (Atul). Vedic only; Western astrology is out of v1.

## Read before working
- `docs/build-document-v1.md`: requirements, architecture, calculation spec, test plan
- `docs/career-timing-report-spec.md`: product flow, free-question rules, ad rules
- `docs/decisions-and-open-questions.md`: what is decided, what is only assumed, what is open
- `tasks/`: the milestone you are working on (M0 first)

## Stack (recommended in the build document)
- Frontend: Angular. Android later via Capacitor.
- App backend: Node.js (TypeScript)
- Calculation service: Python (FastAPI + Skyfield with a JPL ephemeris), stateless, in `services/calc/`
- PostgreSQL, a Redis-based queue, object storage, HTML-to-PDF with headless Chromium (Devanagari font)
- Payments: an Indian UPI-capable gateway. OTP: WhatsApp first, SMS fallback.

Build commands and test commands go here once they exist. Keep this section current:
- Calc service (run from `services/calc/`, after the setup in its README):
  - Tests: `.\.venv\Scripts\python.exe -m pytest`
  - Lint: `.\.venv\Scripts\python.exe -m ruff check .`
  - Run: `.\.venv\Scripts\python.exe -m uvicorn calc.main:app --reload`

## Non-negotiable rules
1. The LLM never calculates planetary positions, dasha dates, or transit dates. It only narrates structured data produced by the calculation service and the rule table.
2. The "show the math" appendix is generated deterministically from calculation output and the rule table, not by the LLM.
3. Do not invent astrological rules. The rule table (`data/rules/`) is authored and reviewed by a practising astrologer. If a rule is missing or ambiguous, stop and ask the founder; do not fill it in from general knowledge.
4. Every conclusion about chart accuracy comes from the golden test set (`data/golden/`), not from reasoning. If golden cases do not exist yet, say so and stop at that point.
5. Calculation conventions (ayanamsa, mean vs true node, dasha year length, dasha balance method, house system) must be explicit, configurable, recorded in `docs/decisions-and-open-questions.md`, and stored as `engine_version` with every chart and report.
6. Guardrails run before any free or paid answer. Blocked: health outcomes, death, "should I invest/put savings", legal outcomes. Self-harm gets a crisis-resource message, not a plain refusal. (Founder assumptions, not yet confirmed.)
7. Language in reports: favourable or difficult periods, never promised outcomes, no fear-based wording, no health, death or investment advice.
8. Birth data tied to a phone number is personal data. Do not log it. Do not put real user data in tests, fixtures or prompts. Store only what the build document says.
9. No secrets in the repo. Use `.env` (see `.env.example`); never commit `.env`.
10. Never call external services from the calculation service at runtime. Ephemeris files are local.

## Working agreements
- Start every milestone or large task in plan mode. Propose the plan, wait for approval, then implement.
- Work in small tasks from `tasks/`. One task, one commit, with tests passing.
- Write tests first for calculation code. Report test results honestly, including failures and skipped cases.
- When a convention or astrological question is open, list the options and ask; do not choose silently.
- Keep changes scoped to the task. Do not refactor unrelated files.
- At the end of a task, summarise: what changed, what was tested, what is still unverified.
- Update `docs/decisions-and-open-questions.md` whenever a decision is made or an assumption is confirmed.
