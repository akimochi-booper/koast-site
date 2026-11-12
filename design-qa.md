# Website Voice Shelf QA — November12

Selected target: shared `mockups/shared/2026-11-11-voice-feedback/displayed-3-voice-shelf.png`, exact displayed option3. Scope is microphone feedback only. Existing neutral composer, native typography,44px Satin Corner Send, bubbles and popup geometry are retained intentionally.

Compared source and actual390/320 screenshots together in the root review. The generated1239x1238 conceptual composition is normalized to its voice component; it is not a phone viewport or a specification to replace existing bubble/composer sizes. Actual browser capture dimensions were confirmed390x844/320x720 at device CSS resolution. Desktop1440x900 also reviewed. Evidence is in shared `audits/2026-11-12-voice-shelf/site-local-*.jpg`.

- Typography: existing website font and16px input preserved;12px status and tabular elapsed timer legible, no clipping.
- Spacing:48px shelf occupies its own layout row with4px clearance immediately above the native composer;44px Cancel hit area, flexible measured waveform, no overlay or page overflow.
- Tokens: teal waveform/Stop and neutral surface follow the selected direction. Existing teal focus rim and upper-corner Send glint retained.
- Assets: native Close glyph reused; waveform is functional canvas data from the analyser, not a replacement for a raster asset or simulated volume. No illustrative assets added.
- Content: actual Starting/Listening/Finishing and recovery states; Cancel restores original draft, Stop keeps dictated text, explicit Send fences late callbacks. Unsupported speech hides the microphone.

Native browser actions checked Cancel, Stop, draft retention, narrow growth, focus and existing explicit Send behavior through local fixture. Synthetic speech and a real oscillator/analyser pipeline were visibly labelled; no microphone permission was requested. Real iPhone/browser recognition acceptance remains separate.

No P0/P1/P2 finding remains in the scoped design. Existing website page/popup styling and accepted Send remain intentional app-specific adaptations.

final result: passed
