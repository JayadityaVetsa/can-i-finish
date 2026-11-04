## Inspiration
A service can be available and still feel out of reach. Someone finds the page they need, follows the interface, and gets stopped at the last control. That moment can turn an ordinary task into asking another person for help. We want the last step to belong to the person taking it.

## What it does
Can I Finish brings task-completion intelligence to keyboard accessibility. Give a browser journey a concrete finish line. Run real keyboard input, replay screenshots and focus evidence, review an on-device AI repair proposal, and rerun the same contract after changing the code. Export a regression test so the repair goes into the next release.

## Real journeys
We followed GOV.UK to a disabled person's bus-pass application page: 26 key events, 28 evidence frames, destination confirmed. We reached Apple's actual iPhone VoiceOver setup article using the keyboard. Then we tested our Field Notes merchant checkout: 18 Tab presses missed the broken control; a native-button repair reached PayPal in four key events.

## How we built it
Node.js and Playwright execute the contracts; the viewer links each input to browser evidence. Qwen2.5-Coder runs locally through Transformers.js to review supplied findings and source. A PayPal sandbox Orders API integration creates, captures and verifies a one-dollar digital-notebook purchase. Measured outcomes come from browser assertions.

## Why it matters
A screenshot helps explain a barrier. A repeatable task helps a team fix it and keep it fixed. The aim is simple: build a web people can finish.
