# Calculation service: rules for this folder

This file loads when Claude Code works in `services/calc/`. The root `CLAUDE.md` still applies.

- Pure functions where possible: same input gives the same output. No network calls at runtime. No database.
- All conventions (ayanamsa, node type, dasha year length, dasha balance method, house system) are explicit parameters with a recorded default. Never hard-code a convention silently.
- Return `engine_version` in every response. Bump it whenever any calculation or convention changes.
- Dates: store and return UTC; also return local time with the timezone name used.
- Write the test first. Boundary cases matter: values just under and over a sign or nakshatra boundary, midnight births, daylight or wartime clock changes, leap days.
- Tolerances live in one config file and are compared against `data/golden/`. Do not loosen a tolerance to make a test pass; report the miss and ask.
- Do not add interpretation, scoring or text here. Interpretation belongs to the rule table and the report pipeline.
- When a result looks plausible but you cannot check it against the golden set, say it is unverified.
