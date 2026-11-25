# Astrology App: decisions and open questions
Last updated: 2026-11-25 (starter kit copy)

## Decided (by the founder)
- Audience for v1: Vedic only. Western astrology is out of v1.
- Core promise: timing predictions (when a problem eases)
- Engine: real chart calculation (open-source ephemeris + own Vedic layer), then LLM interprets the computed chart
- Business: paying business, pay per question or report
- First product: Vedic Career Timing Report (see career-timing-report-spec)
- Model: first question free, then paywall for the full report
- Acquisition: Instagram and Meta ads
- Budget: runway is not a constraint, but spend should be restricted; the test budget decision is deferred
- v1 scope: web funnel plus Android app, built web first and Android last
- Builder: solo, full-time, using Claude Code in a terminal on a laptop; code kept local
- Languages at launch: English and Hindi
- Birth time: support exact, approximate, and unknown (Moon-based)
- Report delivery: downloadable PDF
- Stack: founder asked Claude to recommend; recommendation is in build-document-v1 (Angular + Capacitor, Node.js backend, Python calculation service, PostgreSQL)
- Astrologer review: one paid rule author plus two independent checkers (recommended; reviewers not yet chosen)

## Assumed (founder has not confirmed; change if wrong)
- Sensitive questions (health, death, "should I invest"): app declines with a short non-answer and points to a doctor or advisor
- Timing predictions are framed as favourable/difficult periods, with the dasha or transit logic shown. No promised dated outcomes.

## Conventions to decide in M0 (record the choice here)
- Ayanamsa: default Lahiri (confirm against reference software)
- Node type: mean or true
- Vimshottari year length: 360 or 365.25 days
- Dasha balance method
- House system: whole-sign (default)

## Decided in M0
- Ephemeris kernel (T2, 2026-11-25): JPL DE440s (`de440s.bsp`, 32,726,016 bytes). Read from the file itself, its range is 1849-12-25 to 2150-01-21 UTC, which covers the required 1900-2100. Chosen over full DE440 because it is far smaller (about 32 MB) and the extra range is not needed. Fetched once by `services/calc/scripts/fetch_ephemeris.py`, not committed. SHA-256 recorded for reference only (not checked against a published value): `c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2`. Whether DE440s accuracy suffices for the Moon is unverified; to be judged against the golden set in T4, not assumed.

- Local time handling (T3, 2026-11-25; founder accepted the proposed defaults): the calc service takes an IANA timezone name in the request and never derives it from coordinates (place search is a backend job, FR1). Nonexistent local times (clock-forward gap) and ambiguous ones (clock-back overlap) are rejected with a clear error; no `fold` choice is guessed. Offsets come from the IANA tz database via the `tzdata` package (installed version 2026.6). A tz database update can change historical offsets, so the tzdata version is a calculation input; it is not yet part of `engine_version` (to be handled at T11). Historical Indian offsets are unverified until golden cases exist.

## Open risks and unanswered questions
1. Accuracy: needs the golden-set test plan in build-document-v1 before any paid launch.
2. Unknown or approximate birth time makes dasha timing unreliable; see the confidence model in build-document-v1 section 5.
3. Astrologer reviewers: not yet chosen; fee and scope open.
4. Unit economics: LLM cost per free answer and per report vs a Rs 199-299 price after GST and payment fees. Not yet measured.
5. Test budget and ceiling on cost per paid report: deferred.
6. Free-question abuse and cost: OTP gating and daily caps are in the spec.
7. Meta ad rejection risk: ad copy must avoid personal-attribute claims.
8. Google Play billing rules for selling reports inside the Android app (matters at the last milestone).
9. Data protection (India DPDP Act) and legal review before launch.
10. Competition: other sellers already list career timing; differentiation is dated windows with the math shown.
11. Price (Rs 199 vs 299), refund wording.
