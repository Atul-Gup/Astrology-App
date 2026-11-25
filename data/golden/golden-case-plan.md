# Golden case plan: 45 cases

Purpose: a list of what to cover, so the golden set exercises the hard parts of the calculation, not just ordinary charts. Use invented birth details (no real people). Claude has not computed any chart values; every reference value must come from your reference software.

| Group | Count | What to choose | Why it matters |
|---|---|---|---|
| Ordinary charts | 10 | Birth years spread over 1965-2008, in Mumbai, Delhi, Bengaluru, Kolkata, Chennai, Hyderabad, Pune, Lucknow, Jaipur, Patna; mixed times of day | Baseline accuracy; most users look like this |
| Moon near a nakshatra boundary | 6 | In the reference software, search for dates when the Moon is within about 0.1 degree of a nakshatra boundary, on both sides of the boundary | A tiny error changes the starting dasha lord |
| Moon near a sign boundary | 4 | Moon within about 0.1 degree of a sign boundary, both sides | Decides the Moon sign and Sade Sati status |
| Ascendant near a sign boundary | 4 | Pick a time when the ascendant is within a few arcminutes of a sign boundary, both sides | Birth-time sensitivity; lagna can flip within minutes |
| Near midnight and date changes | 4 | Births at 23:50, 00:05, plus one on a leap day and one on 31 December | Date and timezone conversion bugs |
| Historical Indian clock offsets | 4 | Births in years when India's clock offsets differed from today's (check the timezone database for which years), in Kolkata, Mumbai and Chennai | Tests the historical timezone logic |
| Outside India | 3 | London and New York (one in summer, one in winter) and Dubai | Daylight-saving handling and non-India timezones |
| High latitude | 3 | One in northern Europe, one far south, one near the equator | Ascendant and house calculation at extremes |
| Transit edge cases | 3 | A 12-month window where Saturn or Jupiter is retrograde across a sign boundary; one where Sade Sati starts; one where it ends | Ingress dates and retrograde handling |
| Time confidence | 4 | One approximate time with a stable result; one approximate time where the result changes; one unknown time with a stable Moon sign; one unknown time where the Moon changes sign that day | Tests the Type A, B and C logic |

Total: 45.

## How to fill it
1. Record each case in `golden-charts-template.csv` (rename the filled file `golden-charts.csv`). Use the case ID format `G01` to `G45`.
2. Run each case through two reference programs with the same settings. Write down both values where they differ and add a note.
3. For the time-confidence cases, record what each reference program shows for the start, middle and end of the time range.
4. Keep the settings you used (ayanamsa, node type, house system, dasha year length) in the notes column or a separate settings file.

## What Claude Code will do with it
It compares service output to your reference values within the agreed tolerances (starting at 1 arcminute for longitudes and 1 day for dates) and reports every miss. It cannot create the reference values.
