# Astrology App v1: Build Document (product requirements + technical design)
Status: draft 1, 2026-11-25. Owner: Atul. Companion docs: career-timing-report-spec, decisions-and-open-questions.

## 1. What we are building
A web funnel plus an Android app that sells one product: the Vedic Career Timing Report. A user enters birth details, verifies by OTP, asks one career question for free, gets a partial answer, then pays (Rs 199-299 test) for the full 12-month timing report as a downloadable PDF, in English or Hindi.

In scope for v1: web funnel, Android app, OTP, free question, guardrails, payments, PDF report (English/Hindi), basic admin, analytics.
Out of scope for v1: Western astrology, marriage matching, remedy shop, live astrologers, WhatsApp chat channel, regional languages beyond Hindi, iOS.

## 2. Decisions this document rests on
- Report: Career Timing (Vedic: Vimshottari dasha + Saturn/Jupiter transits)
- Free first question, then paywall; delivery as PDF
- Platforms: web first, Android last (confirmed by founder)
- Birth time: exact, approximate, or unknown (Moon-based) all supported
- Acquisition: Instagram/Meta ads. Budget decision deferred.
- Solo builder, full-time. Languages: English + Hindi.
- Western astrology: out of v1 (confirmed by founder)

Recommended stack (Atul asked for a recommendation):
- Frontend: Angular. Android app: the same Angular code wrapped with Capacitor, so there is one UI codebase.
- App backend: Node.js (TypeScript). Handles auth/OTP, orders, payments, LLM calls, report jobs, admin.
- Calculation service: small Python service (FastAPI + Skyfield with a JPL ephemeris), stateless: birth data in, chart JSON out. Reason: planetary accuracy matters (see section 6), and Python has the best open-source astronomy and testing tools. Keep it small so the second language is a minor cost.
- Database: PostgreSQL. Job queue: Redis-based (e.g. BullMQ). File storage: object storage with signed URLs.
- PDF: render an HTML template to PDF with headless Chromium, using a Devanagari font for Hindi.
- Payments: an Indian gateway with UPI (Razorpay or Cashfree). OTP: WhatsApp authentication message first, SMS fallback (SMS in India needs DLT registration).
- LLM: one provider behind an interface. Smaller model for free answers and guardrail classification, stronger model for the paid report.

## 3. User flow
1. Landing page (from ad). Enter name (optional), date of birth, birth-time confidence, time, place, language.
2. OTP verification (phone). One free question per verified number and per device.
3. Ask one career question (free text or one of ~4 suggested questions).
4. Guardrail check. Sensitive topics get a short decline and a pointer to a professional.
5. Free answer: chart snapshot, current dasha period explained, short answer, current month rating only.
6. Paywall: remaining 11 months, best 2-3 windows, action steps, "show the math" appendix.
7. Payment, then report generation (async), then PDF download and a link on "My reports".

## 4. Functional requirements
Each has a short acceptance test.

FR1 Birth data capture. Place search returns coordinates and a timezone valid for the birth date (historical offsets). Test: births in different decades resolve to the correct offset.
FR2 OTP. Fails safe and rate-limited. Test: 4th request in 10 minutes from one number is refused.
FR3 Free question. One per verified number/device; question stored with the chart. Test: second attempt shows the paywall, not a new answer.
FR4 Guardrails. Classifier runs before any answer. Blocked: health outcomes, death, "should I invest/put savings", legal outcomes, self-harm (this one gets a crisis-resource message, not a refusal). Test: 30-question red-team set, all blocked correctly.
FR5 Chart calculation. See section 6.
FR6 Free answer. Never contains dated windows beyond the current month. Test: automated check that the free answer has no month ratings other than the current one.
FR7 Payment. Order created before payment; report is generated only after the gateway confirms by webhook. Idempotent. Test: duplicate webhook produces one report.
FR8 Report generation. Two report types (section 5). Async job with retry. Test: failed LLM call retries, then flags for manual review rather than delivering a broken PDF.
FR9 PDF. English and Hindi, correct Devanagari rendering, page numbers, disclaimer. Test: visual check on 5 sample Hindi reports.
FR10 My reports. Sign in by OTP, re-download, regenerate on request (limited).
FR11 Refunds and support. Admin can refund and regenerate. Refund policy shown before payment.
FR12 Admin. Orders list, report regeneration, kill switch for free answers, daily free-answer cap.
FR13 Android. Same flows as web. Payment method must comply with Google Play rules for digital goods (verify before building).
FR14 Analytics. Events: ad_click, landing_view, birth_submitted, otp_sent, otp_verified, question_asked, question_blocked, free_answer_shown, paywall_view, checkout_started, payment_success, report_delivered, pdf_downloaded, refund.

## 5. Birth-time confidence model
The dasha timeline depends on the Moon's exact position, and the Moon moves about 13 degrees a day (roughly one nakshatra). An uncertain birth time therefore shifts dasha dates a lot: a 6-hour uncertainty can move the dasha start by up to a quarter of that dasha's length (years for long dashas). So:

- Type A, exact time (high confidence): dasha + transit windows. Full report.
- Type B, approximate time (medium confidence): compute the chart at the start, middle and end of the stated range. If the current dasha/antardasha months and the lagna stay the same across the range, deliver as Type A, labelled "medium confidence". If they change, deliver as Type C and say why.
- Type C, unknown time (lower confidence, "Moon-based"): timing comes from transits of Saturn and Jupiter relative to the natal Moon sign (including Sade Sati status). Dasha windows are not shown. If the Moon changes sign during the birth date, ask for an approximate time of day or warn that the Moon sign is uncertain. Report states clearly that precision is lower.

An astrologer should confirm this logic before launch.

## 6. Calculation specification
- Sidereal zodiac, Lahiri ayanamsa (default), whole-sign houses, geocentric positions from a JPL ephemeris.
- Moon accuracy matters most. One arcminute of Moon error is roughly 9 days of dasha error for a 20-year dasha. Target arcsecond-level positions; do not use a library that only guarantees about an arcminute without checking.
- Decisions to record and match to the reference software used in tests: mean vs true lunar node; Vimshottari year length convention (360 vs 365.25 days); how the dasha balance at birth is computed.
- Outputs: planet longitudes, sign/nakshatra/pada, lagna, 10th house and its lord, Vimshottari Mahadasha/Antardasha/Pratyantardasha dates, Saturn and Jupiter transit ingress dates and retrograde periods for the next 12 months, Sade Sati status.
- Window scoring: deterministic rule table, not the LLM. Each month is scored using the active dasha lords' relation to the 10th house/lord and transits over the 10th house, Moon and lagna. Every score stores the list of rules that fired. The rule table must be authored or reviewed by a practising astrologer; this document does not supply the astrological rules.

## 7. LLM usage
- The LLM never calculates positions or dates. It receives the computed chart, the month scores and the fired rules as structured data, and returns structured JSON sections (summary, per-window narrative, action steps).
- The "show the math" appendix is generated deterministically from calculation output and the rule table, not by the LLM.
- Automated consistency check after generation: every planet, sign, date and month mentioned in the text must exist in the input data. Fail means regenerate, then manual review.
- Framing rules in the prompt: supportive/difficult periods, no promised outcomes, no health, death or investment advice, no fear-based language, no expensive remedies.
- Hindi: generate directly in Hindi (not translate afterwards); native-speaker review of the first 20 reports.
- Cost controls: cached chart, capped free-answer length, daily cap, per-user rate limit, model per task.

## 8. Data model (main tables)
users(id, phone_hash, created_at) | birth_profiles(id, user_id, dob, time, time_confidence, place_text, lat, lon, tz, language) | charts(id, profile_id, engine_version, json) | questions(id, user_id, profile_id, text, class, blocked_reason) | free_answers(id, question_id, text, model, cost) | orders(id, user_id, profile_id, amount, status, gateway_id) | reports(id, order_id, type, status, input_json, output_json, pdf_url, model, cost) | events(...) | refunds(...)
Store the engine version with every chart and report so old reports can be reproduced.

## 9. Privacy, compliance, claims
- Birth data tied to a phone number is personal data. Collect consent at entry, state purpose and retention, support deletion. India's Digital Personal Data Protection Act applies; get legal review before launch.
- Show a plain disclaimer: guidance based on astrological tradition, not a guarantee, not medical, legal or financial advice.
- Ads: benefit-based copy only (see spec). Do not use the user's data to target ads beyond what Meta's own tools do.
- Store only what is needed; set a retention period for questions and reports.
- Collect GST and payment-gateway requirements before going live.

## 10. Accuracy and test plan (must pass before charging anyone)
- Golden set: 40-50 birth charts including edge cases: near nakshatra and sign boundaries, near midnight, different decades, the historical Indian time offsets, and births outside India.
- Compare against two reference programs (e.g. Jagannatha Hora and one other). Tolerances to start with: planet and ascendant longitudes within 1 arcminute; dasha dates within 1 day; transit ingress dates within 1 day. Investigate every miss.
- Astrologer review of 20 sample reports for correctness and tone.
- Guardrail red-team set of 30+ questions.
- LLM output consistency check (section 7) run on 100 generated reports.
- Hindi PDF visual check.
- Payment tests: duplicate webhooks, refunds, failed payments.

## 11. Milestones (estimates; solo, full-time)
M0 (about 3-4 weeks): calculation service + golden-set tests + rule table drafted with an astrologer.
M1 (about 2-3 weeks): web funnel with a fake payment; free answer; guardrails.
M2 (about 2 weeks): real payments, report generation, PDF in English and Hindi.
M3 (about 2 weeks): admin, analytics, analytics-based fixes, privacy and legal review, soft launch with a few ads and semi-manual QA of every report.
M4 (about 2-3 weeks): Android wrap, Play billing decision, store submission.
These are rough guesses to refine after M0.

## 12. Open decisions (updated 2026-11-25)
Resolved: Western astrology is out of v1; web first, Android last; reviewer structure recommended (one paid rule author plus two independent checkers).
Still open:
1. Test budget and cost-per-paid-report ceiling (deferred by founder).
2. Confirm assumption: sensitive questions are declined with a pointer to a professional.
3. Confirm assumption: timing is framed as favourable/difficult periods, not dated promises.
4. Mean vs true node, dasha year convention (match the reference software).
5. Play Store payment approach.
6. Price: Rs 199 vs Rs 299.
7. Refund policy wording.
8. Astrologer reviewers: not yet chosen; fee and scope open.
