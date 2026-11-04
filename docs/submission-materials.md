# Submission materials — review state

No event has been submitted. First submission must be Next Byte Hacks V5. Later entries disclose the same project and reused code. These materials do not replace each event's final eligibility check or required agreement.

## Shared links

- Source and complete local setup: https://github.com/JayadityaVetsa/can-i-finish
- General review video, captions and transcript: https://github.com/JayadityaVetsa/can-i-finish/releases/tag/pitch-v4-review
- PayPal review video, captions and transcript: https://github.com/JayadityaVetsa/can-i-finish/releases/tag/pitch-v4-review
- Vercel URL: https://can-i-finish.vercel.app (public Hobby deployment; viewer, downloads, API configuration and real sandbox create/cancel verified).
- YouTube URLs: pending entrant approval and upload. PayPal requires a publicly visible YouTube video.

## Next Byte Hacks V5

Title: Can I Finish?

Pitch: Find the keyboard barrier that stops a real task. Replay browser evidence, compare a fix, and keep a regression test so people can finish independently.

The existing draft (1277600) has this title, a new thumbnail, three new gallery images, an updated project story, and the source/review links. Four old AccessKit gallery images await deletion confirmation. The Vercel link is saved; the YouTube field remains pending. Do not accept final terms or submit before the entrant approves the video and supplies its link.

## Remote Control AI — proposed description

Choosing a course or reaching checkout should not end with asking somebody else to operate the page. Can I Finish helps developers reproduce a specific keyboard barrier, inspect the evidence, and verify a repair.

An explicit task contract runs through real Chromium keyboard events. Each input produces a screenshot, focus metadata and timestamp. Matched before/after runs demonstrate a registration control missing from sequential focus, a dialog that ignores Escape, and an owned storefront's PayPal sandbox handoff. A separate Apple VoiceOver-guide journey provides a public-site example.

An experimental Qwen2.5-Coder model runs locally in a WebGPU worker. It explains supplied runner findings and relevant source, drafts an unverified suggestion, and cites evidence steps. It does not independently discover the fixture bug or control measured pass/fail. Its native-button proposal matches a correction independently exercised by the browser runner. Model prose can still be wrong; this limitation is explicit.

Developers can export evidence, contracts and executable keyboard regressions. The project is free to run locally, with no paid model API. Nineteen automated checks pass. Results concern the displayed task and browser; there is no full accessibility certification or fabricated user-study claim.

Use the PayPal/AI cut if accepted by the entrant. Recheck whether the event considers this AI explanation sufficiently central; do not claim unbuilt autonomous planning or repair. Disclose the earlier Next Byte entry and development dates. Registration and event-specific terms are pending.

## PayPal AI Hackathon — proposed story

### Problem and audience

A merchant's final checkout action can work with a mouse while being absent from keyboard focus. Developers need a reproducible task and evidence of the barrier before a customer needs help finishing.

### Working prototype

Can I Finish sends keyboard input through Chromium, captures screenshots and focus traces, and compares the same contract before and after a merchant-control correction. The owned broken storefront fails to reach its checkout action after 18 Tabs; the corrected version reaches PayPal sandbox sign-in in 3 key events. This contract stops at sign-in and does not certify the remainder of PayPal's interface.

The actual sandbox Orders API integration creates orders, redirects to buyer approval, binds an order to a signed session, checks the expected USD1.00 amount and completion states, and captures with an idempotency key. The entrant manually approved a fictional test purchase. A subsequent API read verified both COMPLETED order and capture states. A separate returned order had no capture; a native keyboard cancellation recording also passed. No real money is involved.

### AI functionality

The local Qwen model explains supplied runner findings and optional owned source, proposing an explicitly unverified change. The recorded native-button proposal matches the fixture correction, whose outcome is established by a browser rerun. This is an experimental developer-assistance feature, not independent defect discovery or automatic payment approval. No paid model API is required; WebGPU and an initial model download are required.

### Implementation and disclosure

Node.js, Playwright, vanilla JavaScript/HTML/CSS, Transformers.js, WebGPU, PayPal sandbox Orders API, and Vercel Functions. Original code is MIT licensed. Codex assisted with code, tests, interface and documentation. Kokoro generated the narration. Third-party libraries and models retain their licenses.

Explain the project chronology accurately: the keyboard-lab core began November 1; PayPal integration and verification were added November 2. Disclose the earlier Next Byte submission when it occurs. Existing-project acceptance does not remove the obligation to describe reused work.

### Verification and limits

19 automated checks cover artifact integrity, contract limits, output-reference validation, merchant handoff evidence and mocked payment protections. Live sandbox approval/capture and cancellation were checked separately. No user study, broad AI accuracy, screen-reader coverage or WCAG certification is claimed. Public evidence uses shortened payment references and removes sandbox URL query strings.

An existing registered PayPal draft (1273895, initially “Some project”) was found. Eligibility acknowledgements, final deployment URL and public YouTube URL remain pending. Do not submit until those are ready and the entrant approves the video.

PayPal overview, story and technical additional-information fields were saved to draft 1273895-can-i-finish on November 2. Residence, optional-sponsor selection, feedback/learning answers, final media and eligibility review still need completion. No final agreement was accepted.

## Registration and draft continuation

Remote Control AI registration was completed after the entrant explicitly approved its eligibility and Official Rules/Devpost Terms agreement. Draft 1279852-can-i-finish is saved with a 251-word description, live demo/source links, thumbnail and two evidence images. Its public preview is https://devpost.com/software/can-i-finish . No final agreement or project submission was made.

The entrant supplied the remaining PayPal residence and feedback answers; these were saved and verified after reopening the form. Optional sponsors are accurately disclosed as none. Final eligibility attestations and final submission agreement remain for review.

Remaining dependencies: entrant video approval and YouTube links; removal confirmation for four old Next Byte AccessKit images; final eligibility/rule review and submission agreements. Next Byte must be submitted first, then actual entry chronology must be reflected in later entries.
