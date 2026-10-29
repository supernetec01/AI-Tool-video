# Repository validation — 2026-10-29

Validated from this repository checkout after copying the original project:

- `npm ci` completed against the committed lockfile.
- Python 3.12 virtual environment installed all pinned `requirements.txt` packages.
- `npm run check` passed.
- Remotion rendered frame 650 from `src/index.ts`; its pixels exactly matched the reviewed original frame.
- Jianying export rebuilt both main and 2-second smoke drafts using the unchanged verified 60-second clean plate, avoiding another full video render.
- Validator passed timeline continuity, all primary and auxiliary material references, 52 native text segments, device-neutral paths and metadata, retained image comparisons, and simulated Windows/Mac installer safeguards.
- Packaging rebuilt and integrity-checked the 31-file ZIP copied to `deliverables/MomBite01-Jianying.zip`.

The MP4 deliverables are the previously reviewed full renders, not new full renders from this checkout. Native Jianying Desktop opening, font geometry, editing and export still require the recipient smoke test; no actual Windows/Mac app testing is claimed. Spoken narration remains absent as documented in the README.
