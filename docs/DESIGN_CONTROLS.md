# Design controls

Design is a validated Pydantic model and a matching TypeScript interface. Coordinates and font sizes target the selected output frame: landscape 1920 × 1080, portrait 1080 × 1920 or square 1080 × 1080, regardless of browser size. PATCH config replaces the entire model; omitted fields get defaults. Older JSON files work through those defaults.

| Group | Fields and meaning |
| --- | --- |
| Context | title (120 characters), description (1200), atmosphere (300), image_style illustration/realistic |
| Visualizer | visualizer waveform/spectrum; color #RRGGBB; sensitivity 0.2–4; wave_y 0.3–0.65 and wave_height 0.06–0.22 are canvas fractions |
| Title | title_font; title_bold; title_font_size 28–110 px; title_offset_x −600…600 px and title_offset_y −80…400 px |
| Subtitles | subtitle_font; font_size 28–72 px; subtitle_color; outline 1–6; subtitle_margin 40–180 px; subtitle_width 0.5–0.9; max_lines 2/3 |
| Timing | trim_subtitles requires explicit permission; highlight_words and highlight_color use estimated model word timing when available |
| Logo | six logo_position choices, logo_margin 20–160 px; only relevant when a logo was uploaded |
| Encoding | crf 18–28 (lower is higher quality); preset ultrafast/veryfast/fast/medium |

The title anchor is top-center at (frame_width / 2 + title_offset_x, 100 + title_offset_y). Wrapping width shrinks near the edges, up to 1600 px. Titles are limited to three lines and must fit above the visualizer. Large offsets may require shorter text or smaller type. Subtitle/visualizer overlap is also rejected.

Included families: DejaVu Sans/Serif/Mono, Nunito, Fredoka, Rounded (derived from Quicksand), Poppins, Baloo 2, Outfit, Balsamiq Sans, Lexend, Atkinson Hyperlegible and Comic Neue. Each includes Regular/Bold files. Comic Neue is a libre Comic Sans-style alternative, not Comic Sans MS. Fonts are used by browser composition, Pillow measurement and libass rendering. See THIRD_PARTY_NOTICES.md for licenses and provenance.

Save settings, approve background and render a new preview after changes. The composition canvas approximates the output; the rendered MP4 decides exact font wrapping and timing. Exported JSON contains only settings, not the background, logo, media or current session. UI language/theme do not belong to Design.

## Visual editing and formats

output_format selects landscape, portrait or square and is part of the exported Design. The render graph scales/pads the background, computes the visualizer from frame dimensions and sets matching ASS resolution; output is validated against that exact size. Keep a newly approved preview for each format. Uploaded backgrounds retain source aspect so a true portrait image is not normalized into a permanent landscape letterbox first.

Drag title/logo on the canvas, use arrow keys (10 px; Shift 50 px), or use the existing controls. Corner handles resize the title (font pixels) and logo (scale). Alignment guides appear during drag. Free logo_x/logo_y are normalized top-left fractions; renderer and composition clamp to frame bounds using actual normalized logo size. Choosing a preset resets free coordinates. logo_scale ranges 0.25–2.5. Title dragging stays within the same safe offset limits; preflight rejects text that cannot fit after wrapping.

Preflight measures actual title text, validates all caption wrapping and warns about likely logo/title/subtitle/visualizer overlap. It does not recognize faces or replace watching the rendered preview. The small subtitle timeline represents cue intervals, not an acoustic waveform or forced alignment. Editing SRT/timing removes estimated word highlighting and requires approval again.
