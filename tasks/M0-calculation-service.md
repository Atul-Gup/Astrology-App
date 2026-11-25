# M0: Calculation service and golden tests

Goal: a stateless Python service in `services/calc/` that takes birth data and returns a chart, dasha timeline and 12-month transit data. It must match reference software on the golden set before anything else is built on it.

Estimate in the build document: about 3-4 weeks solo. Treat as a guess until T4 is done.

## Your tasks (the founder, not Claude Code)
- H1. Create the golden set in `data/golden/` (see its README). Claude Code cannot produce reference values; they must come from established software.
- H2. Open the reference software's settings and write down: ayanamsa, node type, dasha year length, house system, dasha balance method. Give these to Claude Code for T4-T8.
- H3. Start choosing the astrologer reviewers and the school (default: Parashari, Lahiri, Vimshottari).
- H4. Start the rule table with the author in `data/rules/rule-table-template.csv`. M1 needs a draft; M0 does not block on it.

## Claude Code tasks
Each task ends with tests passing, one commit, and an update to the decisions doc if a convention was decided.

### T1. Scaffolding
FastAPI app, test runner, linter, a health endpoint, and a README in `services/calc/` with run and test commands. Update the "Build commands" section of the root `CLAUDE.md`.
Done when: tests and linter run with one command each.

### T2. Ephemeris loading
Load a JPL ephemeris kernel locally (no network at runtime). Choose a kernel that covers at least 1900-2100 and record which one and why. Load once at startup.
Done when: the service returns positions for a test date and a test asserts the kernel's date range is enforced with a clear error.

### T3. Time and place
Convert local birth date, time and place (latitude, longitude, timezone name) to UTC using the IANA timezone database, including historical offsets. Reject impossible or ambiguous local times with a clear error (for example, clock changes).
Done when: tests cover several decades and at least the historical Indian time cases you list in the golden set.

### T4. Planet positions
Apparent geocentric ecliptic longitude of the Sun, Moon, Mercury, Venus, Mars, Jupiter and Saturn, converted to the sidereal zodiac with the chosen ayanamsa. Record the exact ayanamsa definition and its source in code comments and the decisions doc.
Done when: the golden set shows differences within tolerance (starting tolerance: 1 arcminute; target arcsecond-level for the Moon).

### T5. Lunar nodes
Rahu and Ketu, using the node type chosen in H2. Make mean vs true configurable.
Done when: golden cases pass with the chosen type and a test shows the other type also runs.

### T6. Ascendant and houses
Ascendant from local sidereal time, obliquity and latitude. Whole-sign houses. 10th house and 10th lord.
Done when: ascendant within tolerance on the golden set, including near-midnight and high-latitude cases.

### T7. Sign, nakshatra, pada
For every body and the ascendant. Include boundary tests: values just under and just over a boundary.

### T8. Vimshottari dasha
Dasha balance at birth, then Mahadasha, Antardasha and Pratyantardasha timelines. Year-length convention configurable. Return dates in UTC and local time.
Done when: dasha dates are within 1 day of the reference on the golden set.

### T9. Transits
For a given 12-month window: Saturn and Jupiter sign ingress dates, retrograde start and end dates, and Sade Sati status relative to the natal Moon sign.
Done when: ingress dates are within 1 day of the reference.

### T10. Birth-time confidence model
Implement Types A, B and C from build document section 5. Type B computes the chart at start, middle and end of the stated time range and checks whether the lagna and the current dasha/antardasha months stay stable. Type C returns Moon-sign-based transit data and no dasha windows; it must flag the case where the Moon changes sign during the birth date.
Done when: unit tests cover stable, unstable and Moon-sign-boundary cases.

### T11. API
Endpoints for chart, dasha timeline, and transit window, with a documented JSON schema and an `engine_version` in every response. Input validation and clear error codes.
Done when: OpenAPI docs are generated and contract tests pass.

### T12. Golden test harness
Load `data/golden/` and compare every field to the service output with configurable tolerances. Produce a readable report listing every miss.
Done when: the report runs in one command and fails the build on any miss.

### T13. Hardening
Determinism (same input, same output), no network calls at runtime, input fuzzing for dates and coordinates, and a simple performance check (a chart in well under a second is the aim; measure and report).

## Definition of done for M0
- All golden cases pass within the agreed tolerances, or each miss has a documented, founder-approved reason.
- Conventions are recorded in the decisions doc.
- No astrological interpretation code exists yet. Interpretation arrives with the rule table in M1.
