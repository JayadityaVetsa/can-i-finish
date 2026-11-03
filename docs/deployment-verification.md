# Public deployment verification — November 2, 2026 (Chicago)

Deployment: https://can-i-finish.vercel.app

The free Hobby deployment serves the static evidence viewer and the PayPal sandbox function. Browser automation remains local. The following checks used an isolated, unauthenticated Chromium context rather than the signed-in Vercel session.

| Boundary | Observed result |
|---|---|
| Public viewer | Captured screenshot evidence rendered; no login required |
| AI cancellation | Loading stopped and measured browser outcome was preserved |
| Checkout keyboard control | Corrected native button reached and activated with keyboard events |
| UI → function → PayPal | Production function created a real sandbox order and redirected to sandbox approval |
| Cancellation → UI | PayPal cancellation returned to the canonical HTTPS storefront with an explicit cancelled state |
| Order binding | Capture request with a mismatched order was rejected |
| Origin check | Unexpected origin was rejected with HTTP 403 |
| Video downloads | Both players and downloadable MP4s served publicly |
| Model failure | Blocking the runtime import produced a clear error without changing browser outcome |

The deployed flow did not approve a new purchase. The separately documented local sandbox success was approved manually by the entrant and verified with an independent Orders API read. Capture retries and invalid signed sessions are covered by mocked service tests; there is no claim that duplicate live captures were performed.

Nineteen automated checks pass, including a new regression for model repairs contradicting passing outcomes.

## AI quality observations

The deployed model downloaded and ran in WebGPU. Its first checkout response contained malformed JSON and was rejected. Plain-language output instructions were added, after which the checkout response passed structural and evidence-reference validation. It recommended a native button; extra details such as using submit type remain unverified and are unnecessary for this click handler.

A dialog response cited supplied evidence but incorrectly explained normal focus containment. It does not establish a correct diagnosis or repair. The known browser finding is failure to dismiss on Escape and continue the defined task. This illustrates why structural JSON validation is not semantic validation, and why AI remains visibly unverified.

The passing-dialog model response incorrectly claimed failure and proposed a timeout. It was treated as a failed quality check. A guard now rejects repair proposals for passing outcomes, and the interface disables repair generation for passing runs with an explicit explanation. A regression check covers this contradiction.

The earlier recorded registration suggestion correctly proposed a native button. Passing and empty-evidence inputs, invalid evidence references and immutable outcomes are also covered by the diagnosis unit checks; those checks are not proof of model accuracy. No overall model-accuracy claim is made.

## Media and source

General v3: 177.70 seconds, H.264/AAC, 1920×1080, 30 fps. Full decode completed without errors. The changed AI scene was visually inspected; unchanged scenes retain the prior review. PayPal cut: 172.55 seconds with the same output format, separately decoded and visually inspected. Caption/transcript files and original browser recordings are preserved. Both cuts still await entrant approval.

Source snapshot for public media: 12d6a26. No event was submitted. Remote Control AI registration and the entrant-supplied PayPal residence/feedback fields are now saved. Old AccessKit gallery removal confirmation, video approval, YouTube links, and final event eligibility/submission agreements remain pending.
