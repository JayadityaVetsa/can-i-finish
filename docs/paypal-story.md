### Problem and audience

A merchant's final checkout action can work with a mouse while being absent from keyboard focus. Developers need a reproducible task and evidence of the barrier before a customer needs help finishing.

### Working prototype

Can I Finish sends keyboard input through Chromium, captures screenshots and focus traces, and compares the same contract before and after a merchant-control correction. The owned broken storefront fails to reach its checkout action after 18 Tabs; the corrected version reaches PayPal sandbox sign-in in 3 key events. This contract stops at sign-in and does not certify the remainder of PayPal's interface.

The actual sandbox Orders API integration creates orders, redirects to buyer approval, binds an order to a signed session, checks the expected USD1.00 amount and completion states, and captures with an idempotency key. The entrant manually approved a fictional test purchase. A subsequent API read verified both COMPLETED order and capture states. A separate returned order had no capture; a native keyboard cancellation recording also passed. No real money is involved.

### AI functionality

The local Qwen model explains supplied runner findings and optional owned source, proposing an explicitly unverified change. The recorded native-button proposal matches the fixture correction, whose outcome is established by a browser rerun. This is an experimental developer-assistance feature, not independent defect discovery or automatic payment approval. No paid model API is required; WebGPU and an initial model download are required.

### Implementation and disclosure

Node.js, Playwright, vanilla JavaScript/HTML/CSS, Transformers.js, WebGPU, PayPal sandbox Orders API, and Vercel Functions. Original code is MIT licensed. Codex assisted with code, tests, interface and documentation. Kokoro generated the narration. Third-party libraries and models retain their licenses.

The keyboard-lab core began November 1; the PayPal extension and sandbox verification were added November 2. This project is also being prepared for Next Byte Hacks V5 and Remote Control AI; final entry chronology will be disclosed before submission.

### Verification and limits

19 automated checks cover artifact integrity, contract limits, output-reference validation, merchant handoff evidence and mocked payment protections. Live sandbox approval/capture and cancellation were checked separately. No user study, broad AI accuracy, screen-reader coverage or WCAG certification is claimed. Public evidence uses shortened payment references and removes sandbox URL query strings.


### Source and review materials

[Source and reproducible setup](https://github.com/JayadityaVetsa/can-i-finish) · [Download the PayPal demonstration with captions](https://github.com/JayadityaVetsa/can-i-finish/releases/tag/paypal-review-v1)
