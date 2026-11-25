# Golden set

40-50 birth charts with reference values from established astrology software. The calculation service must match these before anything else is built on it.

## How to create it
1. Choose two reference programs (for example Jagannatha Hora and one other) and set the same conventions in both: ayanamsa, node type, house system, dasha year length. Record them in `docs/decisions-and-open-questions.md`.
2. For each chart, enter the birth data and copy the values into `golden-charts-template.csv` (rename to `golden-charts.csv`).
3. Where the two programs disagree beyond tolerance, record both values and add a note; do not pick one silently.

## Charts to include
- A spread of birth years over several decades, including pre-1970 and the historical Indian time offsets
- Moon close to a nakshatra boundary and close to a sign boundary
- Ascendant close to a sign boundary
- Births near midnight and near a date change
- Births at different latitudes, including one outside India
- A few approximate-time and unknown-time cases, to test the confidence model

## Privacy
Use consented or public data, or invented birth details. Do not use real customers' data. Do not put anyone's name in the file; use case IDs.

## Columns
See `golden-charts-template.csv`. Add columns for any field the tests need. Longitudes are sidereal degrees (0-360) with decimals; dasha dates are ISO dates.
