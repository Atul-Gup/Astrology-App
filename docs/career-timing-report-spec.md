# Career Timing Report: v1 spec and launch plan
Last updated: 2026-11-25

## Product
Vedic (Vimshottari dasha + Saturn/Jupiter transit) report that shows the best and hardest windows for career moves over the next 12 months, with the logic shown. English and Hindi. Price test: Rs 199 vs Rs 299 (net of GST and payment fees is lower).

## User flow (free first question, then paywall)
1. Landing page from Instagram/Meta ad. Enter birth date, time and place.
2. Verify with phone/WhatsApp OTP (limits free-question abuse; also captures WhatsApp opt-in for the later WhatsApp channel).
3. Ask ONE career question, free text or tap one of ~4 chips (e.g. "Best time to switch jobs?", "When to expect an appraisal or promotion window?", "Job or business?", "When will work improve?").
4. Guardrail check first: health, death, and money-decision questions get a short decline and a pointer to a professional. Timing and career questions proceed.
5. Free answer: chart snapshot (lagna, moon sign, nakshatra), current Mahadasha-Antardasha in plain language, a short answer to their question, and the rating for the current month only.
6. Paywall: the other 11 months, the best 2-3 windows, practical actions and the "show the math" appendix are locked behind the report.

## Free answer rules
- One free answer per verified phone number (and per device as a second check).
- Chart calculation is deterministic and cached. The LLM call is short, with a capped output length and a daily cap on free answers plus a kill switch.
- The free answer must be genuinely useful but must not contain the dated windows.

## Paid report contents
1. Chart snapshot
2. Current Mahadasha-Antardasha and what it means for career
3. Month-by-month view for 12 months (favourable / neutral / challenging)
4. Best 2-3 windows to switch, interview, negotiate or start something
5. Practical steps per window; any remedies optional and low-cost (no gemstone selling in v1)
6. "Show the math" appendix: dasha and transit logic behind each rating

Framing: supportive or difficult periods, never promised outcomes.

## Meta ad rules (benefit copy, no personal-attribute claims)
Meta ads must not assert or imply personal attributes or imply the advertiser knows them, and should focus on product benefits.
Use:
- "See your best months for a job switch in 2027"
- "Free career check from your birth chart: ask one question"
- "Which months favour interviews, and which favour waiting?"
- "Vedic career timing, with the math shown"
- Hindi: "2027 mein naukri badalne ke sabse achhe mahine jaanein"
Avoid: "Is your career stuck?", "Struggling at work?", "Saturn is blocking your career", anything about health or finances, celebrity names.

## Test plan
- Run the landing page and a few ad sets before building the full app; fulfil the first 20-30 orders semi-manually if needed.
- Set a fixed test budget you can afford to lose and a ceiling on cost per paid report. Kill ad sets above it.
- Measure: ad click to birth-details rate, birth-details to OTP rate, free answer to paid rate, actual LLM cost per free answer and per report.
- Selling inside the Android app triggers Google Play billing rules for digital goods. Check them before building payment into the app; web checkout on the landing page avoids this for the test.
