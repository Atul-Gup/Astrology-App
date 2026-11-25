# M1 to M4 outline

Detailed task files for these milestones are written when M0 is done. Use plan mode to turn each outline into tasks, one milestone at a time.

## M1: Web funnel with fake payment (about 2-3 weeks)
- Angular landing page and birth-details form (name optional, date, time confidence, time, place search, language)
- Place search returning coordinates and a historically valid timezone
- OTP via WhatsApp first, SMS fallback; rate limits
- One free question per verified number and per device; suggested-question chips
- Guardrail classifier before every answer; red-team set of 30+ questions
- Free answer: chart snapshot, current dasha period, short answer, current-month rating only
- Rule table loaded from `data/rules/` (needs the astrologer's draft)
- Paywall screen with a fake payment
- Node.js backend, PostgreSQL schema (build document section 8), analytics events
- Automated check: the free answer contains no month ratings except the current one

## M2: Real payments, report generation, PDF (about 2 weeks)
- Payment gateway integration with webhook; order created before payment; idempotent webhook handling
- Report generation job: structured data in, structured JSON sections out, with retries
- Consistency check: every planet, sign, date and month in the text must exist in the input data
- Deterministic "show the math" appendix
- PDF from an HTML template using headless Chromium, English and Hindi, Devanagari font, disclaimer, page numbers
- "My reports" with OTP sign-in and re-download

## M3: Admin, analytics, review, soft launch (about 2 weeks)
- Admin: orders, regenerate report, refund, free-answer kill switch and daily cap
- Funnel analytics from the events list in the build document
- Privacy and legal review (India's DPDP Act), refund policy, disclaimers
- Astrologer review of 20 sample reports; Hindi review
- Soft launch with a few ads; every report checked by hand at first
- Set the test budget and the cost-per-paid-report ceiling before spending

## M4: Android (about 2-3 weeks)
- Wrap the Angular app with Capacitor
- Decide how to sell reports inside the app after checking Google Play's billing rules for digital goods
- Store listing and submission
