# Production credits and reproducibility

These pitches combine genuine browser recordings, original interface design, scripted narration and original title cards. Public-site recordings are independent observations, not endorsements. The PayPal cut uses our own interface and sandbox integration; the deliberate merchant button bug is ours.

- Narration: official [ResembleAI Chatterbox](https://github.com/resemble-ai/chatterbox), MIT license, built-in pretrained voice, generated locally on CPU. No personal voice cloning or paid API. Normal model watermarking retained. Emotion setting 0.72, guidance 0.30, temperature 0.75. CPU text decoder dynamically quantized to int8. Rubber Band adjusts conversational pacing without changing pitch.
- Captions: local faster-whisper word timestamps aligned to the authored scripts; reviewed against the rendered footage.
- Music: original procedural instrumental composition in `compose-pitch-music.py`.
- Website fonts: DM Sans and Manrope, self-hosted with their SIL Open Font License files under `dist/fonts/`.
- GOV.UK material: Crown copyright, reproduced under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Source pages: [driving with a disability](https://www.gov.uk/browse/driving/disability-health-condition) and [bus-pass applications](https://www.gov.uk/apply-for-disabled-bus-pass).
- Apple: independently recorded public keyboard journey to Apple's iPhone VoiceOver guide. No claim of affiliation or a repaired Apple defect.
- AI diagnosis: pinned Qwen2.5-Coder model through Transformers.js; its proposal is separate from measured browser assertions. The saved AI proposal page labels its recorded output.
- Codex assisted with implementation, design, scripts, tests, evidence capture and editing. No invented testimonials or adoption statistics.

## Reproduce

Install FFmpeg with libass and Rubber Band support, Pillow, Python 3.11, CPU PyTorch and `requirements-voice.txt`. Download the official Chatterbox weights to a private local directory. Model weights and raw generated speech are not committed.

1. `python generate-expressive-voice.py --weights PATH_TO_WEIGHTS`
2. `python compose-pitch-music.py`
3. `node record-pitch-v4.mjs` (local server running; requires the preserved native evidence videos)
4. `python align-pitch-voice.py` (optional `VOICE_ASR_CACHE` directory)
5. `python build-pitch-v4.py`
6. `python polish-pitch-pauses.py` (removes measured dead air and remaps both caption formats)

Scripts live beside `general.json` and `paypal.json`; exact edit timings are in the corresponding timeline files. Native footage is 25 fps; final H.264/AAC delivery is 1920×1080 at 30 fps. Navigation sequences that are shortened are labelled in the edit. The final pacing pass removes only low-energy pauses between aligned words; it preserves the uncut master locally. Raw captures, private sandbox URLs and local model caches stay excluded from source control.

The videos await entrant review and YouTube upload. No hackathon entry has been submitted.
