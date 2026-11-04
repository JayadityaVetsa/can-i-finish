# Current implementation — November 3, 2026

## Product and evidence

The public-facing product has been redesigned around task completion and independence: a new landing page, separate evidence lab, polished checkout, AI proposal view and payment verification view. Fonts are self-hosted with OFL licenses. The main experience uses genuine GOV.UK and Apple journeys; original campus fixtures remain available as developer examples.

- GOV.UK bus-pass application journey: passed, 26 key events, 28 hash-verified frames, native recording.
- Apple iPhone VoiceOver-guide journey: passed, 39 key events, 42 evidence frames.
- Current Field Notes merchant pair: blocked after 18 Tab presses before; PayPal handoff reached in 4 key events after. The identical task contract is used for both.
- Actual user-approved sandbox purchase: order and capture completed, USD 1.00 verified. Read-only Orders API recheck on November 3 confirmed both states. Public evidence contains shortened references.
- Fresh cancellation recording returns from PayPal to the merchant in 13 key events.
- 20 automated checks pass. Desktop 1365px and mobile 390px layouts and before/after interactions were checked with no page errors or horizontal overflow.

## New presentation

General v4 and PayPal v2 use rewritten benefit-led scripts, locally generated expressive Chatterbox narration, aligned captions, original music and native browser footage. The general cut demonstrates GOV.UK, Apple and the checkout transformation. The PayPal cut demonstrates the owned digital-notebook store, AI proposal, corrected handoff, verified capture and cancellation. No Apple/GOV.UK footage is used in the PayPal cut.

Scripts, production credits and edit timelines are under `docs/pitch-v4/`. Raw captures and generated speech remain preserved locally and excluded from Git. Downloadable MP4, VTT, SRT, transcript and thumbnail assets are under `dist/media/`.

## Entries

The three Devpost entries remain drafts. Their stories were revised to match the current product; the PayPal gallery includes the current store, AI proposal and receipt views. Video approval and entrant-provided YouTube links remain required before final submission. Next Byte must be submitted first. Its four legacy AccessKit gallery images still await specific deletion confirmation; no irreversible deletion was performed. PayPal final eligibility/terms review remains pending.

The deployment stays free on Vercel Hobby. No paid AI service or paid narration service is used. No winning outcome or prize is guaranteed.
