# Can I Finish?

[Public app](https://can-i-finish.vercel.app) · [Video downloads](https://can-i-finish.vercel.app/downloads.html) · [Implementation notes](docs/implementation-status-2026-11-02.md)

General review cut: 2:58 (v3, including the experimental AI segment). PayPal cut: 2:52. Both use Kokoro synthetic narration and await entrant approval. The sandbox approval/capture and cancellation were verified; AI remains an experimental explanation of supplied runner findings, with one reviewed native-button suggestion. No event has been submitted.


**Keyboard journeys, with evidence you can rerun.**

Define a concrete task, send keyboard input through a real browser, inspect where it stops, and run the same contract after a fix. Built for Next Byte Hacks V5 on November 1, 2026. The entry stays a draft until the user explicitly requests submission.

## What is working

- Local Node.js + Playwright runner with real Chromium keyboard input.
- Explicit task contracts: Tab to an accessible role/name, press keys, assert visible or hidden task states.
- A screenshot and focus record after each input, with a SHA-256 content hash.
- Native browser recording, focus trace, reproduction report, contract export, and generated regression script.
- Hosted/static evidence viewer with screenshot-backed playback, focus inspector, and before/after comparison.
- Two controlled journeys in broken and fixed variants: reach course registration; dismiss an updates dialog and continue registration.
- Local UI can rerun those fixtures or run a supplied contract against a public URL. No authentication automation or personal form filling.

## Run for free

Requires Node.js 20+. Chromium downloads once; no API key or paid service.

```sh
npm ci
npm run build
npx playwright install chromium
npm start
# Open http://127.0.0.1:4174
```

The entry point uses the project-local `.local/browsers` cache when present, otherwise Playwright's normal cache. Set PLAYWRIGHT_BROWSERS_PATH explicitly to override it.

In the local workspace, choose **New browser run**. Choose a fixture, or a public URL and a JSON contract. The hosted site is a recorded evidence viewer; it does not pretend to launch a cloud browser.

```sh
npm run demo       # Executes all four fixture journeys; regenerates dist/evidence/
npm test           # Verifies outcomes, matching contracts, artifact integrity and input validation
node cli.mjs run https://your-test-site.example contract.json
```

The CLI accepts URLs you supply; run against a site you are authorized to test. Contracts can activate controls with Enter or Space. Use test copies of transactional workflows. The local HTTP service binds only to loopback and requires same-origin JSON requests; its custom-URL entry rejects obvious private-network initial URLs. It is not intended as a public remote-browser service.

## How it works

`lib/contracts.mjs` defines the tasks; `lib/runner.mjs` executes them. The runner starts a fresh context, navigates, and uses `page.keyboard.press`. It does not call `click` or `locator.focus()` to reach a target. Page evaluation is read-only observation of focus/CSS/DOM. Target matching uses Playwright's accessible role and name lookup. Focus labels in trace metadata are approximate.

On each key, it captures a PNG, focus metadata, timestamp, and hash. Native video comes from Playwright's context recording. An assertion failure stops the task. A failed dialog-dismiss assertion adds a small explicitly labelled diagnostic probe. The report does not automatically label normal modal focus containment a WCAG violation.

`dist/app.js` renders saved evidence, can import/export report JSON, and connects to `/api/run` only on the local workspace. Static hosting needs no backend. Imported JSON cannot inject HTML or reference arbitrary external screenshot URLs. JSON import alone does not transport its screenshot files; serve the associated evidence folder to retain images.

`npm run demo` produces actual runs. Viewer outcomes and metrics come from those reports, not hardcoded pass/fail states. Both fixture variants share an identical contract. Fixtures intentionally contain the bugs; this is a demonstration, not independent validation on production sites.

## Observed demo results

### A real public-site task

The runner executed this contract against Apple's live public website on November 1, 2026: start at https://www.apple.com/accessibility/ , reach the VoiceOver details using sequential Tab navigation, activate the iPhone setup link, and assert the heading of the actual Apple Support article. It passed in 39 key events, with 42 evidence frames and a 1920×1080 native browser recording. The November 2 rerun captured 38.1 seconds, again with 39 key events and 42 frames. The report and every frame are under `dist/evidence/apple-voiceover*`.

This is an independent, narrowly scoped observation, with no Apple affiliation or endorsement. It does not claim that Apple's website is fully accessible or that we found and repaired an Apple defect. The first diagnostic attempt exposed a navigation race in this runner; that was corrected, and the successful capture came from a fresh context. Only the final successful capture is in the public evidence bundle.

`node record-apple.mjs` repeats the live contract. Website content or focus order can change, so future outcomes need not match this snapshot.

The public `demo.html` provides a 78-second edited screencast with locally synthesized Microsoft Zira narration and readable burned-in captions. It uses real 1080p screen recordings; repetitive footage is condensed. The raw Apple browser recording remains separately available. Video output is 1920×1080 at 30 fps; native browser source is 25 fps. `docs/edit-timeline.json` records edits. This short product demo is below the event's written 2–5 minute submission-video range; a final compliant submission cut remains necessary before submitting the draft.

The source ZIP includes the app, runner, tests, screenshots, and native browser recordings. It excludes the edited MP4 to fit the host's per-file limit. For an offline copy of that demo page, separately download the MP4 from the public demo and place it at `dist/media/demo.mp4`.

### Controlled before-and-after tasks

| Journey | Before | After |
| --- | --- | --- |
| Reach registration | Target not reached after 18 Tab presses; rendered div button has tabIndex -1 | Completed in 5 key events |
| Dismiss dialog and continue | Dialog visible after Escape; diagnostic Tab/Shift+Tab stays on two controls | Completed in 7 key events |

Observed with Playwright 1.64.1 and Chromium 156.0.8078.4 on Windows, viewport 1280×900. Generated reports contain exact capture times and browser versions. Counts reflect these fixtures only.

## Scope and limitations

This is one browser/viewport/keyboard-sequence test, not a full accessibility audit, legal compliance determination, or WCAG certification. A bounded Tab failure can require another documented keyboard sequence. The tool records focus-indicator metadata and screenshots; it does not automatically judge visual contrast. Screen readers, cross-origin frames, complex shadow DOM workflows, mobile, authentication, automatic code repair and natural-language task planning are not validated features.

Screenshots and videos can contain page content. Local runs remain under `reports/`; only controlled demo captures are included in the hosted app. Never publish a private report without reviewing it. Hashes establish content integrity within the bundle, not external trust or third-party certification.

## Differentiation and prior art

Keyboard testing already exists in axe DevTools and open-source Playwright tools. This prototype focuses on task outcome contracts, a small inspectable evidence package, generated keyboard regressions, and matched before/after runs. It does not claim to invent keyboard testing or outperform those tools. Real-user studies and independent evaluation remain future work.

Sources: https://www.deque.com/blog/intelligent-automation-and-the-new-era-of-guided-testing/ ; https://github.com/stevefaulkner/keyboard-vibes ; https://playwright.dev/docs/api/class-keyboard ; https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html

## AI and licensing

Codex assisted in architecture, code, fixtures, tests, interface, and documentation. The original runner is deterministic. A new browser-local Qwen diagnosis worker is being validated; measured outcomes remain browser assertions. Playwright is Apache-2.0 licensed; Chromium and bundled tooling retain their respective licenses. Original project code is MIT licensed. No user interviews, production adoption, or measured user-impact claims are fabricated.

## New checkout development setup

The sandbox service reads PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, CHECKOUT_SESSION_SECRET and PUBLIC_ORIGIN from the environment. See .env.example for names only. Configure the values privately in Vercel; never use live credentials. For local development, use Node 22+ with `node --env-file=.env.local start.mjs`, setting PUBLIC_ORIGIN to the local origin. Vercel uses HTTPS secure session cookies; test the complete approval/capture flow on the configured HTTPS deployment. The sandbox storefront is `/checkout.html`. Until configured it clearly reports setup pending.

Run `npm ci` and `npm run build` to bundle the pinned browser runtime. Open-model weights download from Hugging Face on demand and are not committed. The diagnosis worker uses WebGPU; unsupported hardware fails explicitly. AI output is an unverified suggestion, never a measured test result.
