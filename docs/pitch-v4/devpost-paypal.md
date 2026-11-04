## Ready to buy. Able to finish.
The customer has chosen. The price is right. Then the checkout control never receives keyboard focus. A sale stops, and so does the customer's independence. Can I Finish gives merchants a concrete way to find that moment and repair the journey.

## The working example
Field Notes is our digital-notebook storefront, with an actual Markdown download. Its before-and-after merchant controls demonstrate the workflow: 18 Tab presses miss the deliberately broken div; replacing it with a native button lets the same task reach PayPal in four key events. Screenshots and focus traces show what changed.

## PayPal integration
The sandbox Orders API creates a fixed USD 1.00 order and redirects to PayPal approval. Our server binds the order to a signed checkout session, checks amount and completed capture status, and returns a verified receipt. Capture retries use an idempotency key. Cancellation returns to the merchant to start again. An actual entrant-approved sandbox purchase was verified through the Orders API, with both order and capture completed. The notebook download is available from the receipt.

## AI and evidence
An on-device Qwen2.5-Coder model reviews supplied merchant code and the browser finding, then proposes a repair linked to evidence. Developers apply the change and rerun the browser contract. AI proposals remain separate from the measured result. Exported regression tests keep the finish line in the next release.

## Development history
The project began during these events. The same project is also being prepared for Next Byte Hacks V5 and Remote Control AI. The checkout integration, sandbox verification, on-device diagnosis and payment-specific presentation are documented in repository history.

Build a checkout people can finish—and give the merchant evidence that the repair works.
