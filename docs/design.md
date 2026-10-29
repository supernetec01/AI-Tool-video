# Mẹ Bỉm Thông Thái — Dinh dưỡng mẹ bầu, Tập 01

Mode: autonomous creation, explicitly selected by the user. Source: user's Vietnamese brief (pasted text, 12,108 bytes). This is an educational nutrition short, not a software demonstration or a medical advertisement.

## Brief and decisions
Audience: Vietnamese expectant mothers. Deliver a 60-second 9:16, 1080×1920, 24fps video presenting five foods and their nutrients, with safe preparation and folic-acid guidance. Prioritize understandable Vietnamese and calm, appetizing food imagery. No IQ promise. No raw fish, runny eggs, rare beef, or unpasteurized dairy.

| Requirement | Execution |
|---|---|
| Five foods | Five distinct editorial food chapters, large numbered labels |
| 40–50s versus 50–60s in source | Choose 60s to retain safety guidance and reading time |
| Warm maternal aesthetic | Cream #FFF5EA, peach #E9ADA5, brown #4A3833; sage accent #51634B |
| Typography | Locally bundled Noto Sans regular/bold, supports Vietnamese; equivalent to requested sans-serif |
| Real food look | Generated photorealistic stills with restrained camera animation; not claimed to be live footage |
| Voice | Attempt Vietnamese female TTS using an available legitimate service; if unavailable, preserve complete readable on-screen narration and deliver voice script separately |
| Music | Original gentle instrumental piano bed, no third-party recording required; music-free alternate retains voice and transition sounds |
| Branding | Mẹ Bỉm Thông Thái / Tập 01. mombite.ai appears in brief, use only as supplied label; no invented website features or claims |
| Health claims | Retain support language; no guarantee of intelligence; note dietary folate does not replace recommended folic acid |

## Visual direction and motion
Considered: pastel food editorial (selected), clinical infographic (too institutional), dark cinematic food (too severe). Warm natural light, cream paper background, peach rules and chapter numbers, sage nutrient badges, rounded editorial photo windows, no neon, no cartoon food or medical CGI. User supplies explicit color/font/layout guidelines; static styleframe is generated and inspected before Remotion implementation.

Motion: calm/caring, low energy, symmetrical ease-in-out ~42f, no overshoot or shake. Food crop slowly moves in a different direction per chapter, settles for >=1s. Main type is flat and crisp, no perspective deformation. Opening action >=3s. Closing holds >=1s. Transitions use a clean match cut or a brief cream cover, no repeated impact effects.

## Library inspection and adaptation
Inspected the 124-card gallery index and sequence template promo-energy-arc. That sequence's software launch climax and strong electronic music are inappropriate for the explicit maternal nutrition brief. Intentionally adapt R2/Q7/Q8/S1: avoid kinetic group fly-ins, dark metallic orbit, launch slams and tech-house. Health education favors calm food camera motion and acoustic/piano sound. Vertical typography uses large headings 76–116px, supporting copy 48–58px; sufficient high-contrast reading time rather than applying a landscape 5%-of-height rule mechanically.

Opening uses marker-underline-title, style key marker-underline-title. Read exact reference demos/typography/marker-underline-title/MarkerUnderlineTitle.tsx. Preserve title settling 0–26f, underline 32–42f (10f), seeded dry brush, close to word baseline, static hold >=33f. Recolor peach, adapt to Vietnamese upright text with nearly horizontal stroke. Other scenes use custom food editorial camera moves because UI-centric gallery cards do not fit real food. No claim to reproduce another card's preview.

## Storyboard / single timeline
| Scene | Seconds | Frames (24fps) | Information and main motion |
|---|---:|---:|---|
| Hook | 0–5 | 0–119 | One mother/meal image slowly pushes in. “5 thực phẩm / hỗ trợ não bộ thai nhi”; single marker underline |
| Salmon | 5–13 | 120–311 | Fully cooked salmon; DHA / omega-3; supports brain and vision; gentle close-up push |
| Eggs | 13–21 | 312–503 | Firm hard-boiled eggs; choline; brain and spinal cord; restrained lateral reveal |
| Greens | 21–30 | 504–719 | Cooked broccoli/spinach; folate; neural tube; overhead drift; folic acid reminder |
| Beef | 30–38 | 720–911 | Thoroughly cooked lean beef; iron; oxygen transport; slow diagonal move |
| Dairy | 38–46 | 912–1103 | Milk / plain yogurt; protein and iodine; choose pasteurized dairy; gentle pullback |
| Safe meals | 46–55 | 1104–1319 | Mother and meal; diverse foods, cooked food, prenatal supplements per clinician; no IQ guarantee |
| CTA | 55–60 | 1320–1439 | Clean cream endcard, “Lưu lại cho bữa ăn của mẹ”; folic-acid reminder and series signature |

At 24fps the marker's original 30fps frames are time-scaled by 0.8, retaining its duration in seconds. Title settles at local f17.6 and the second line at f21.6, before the f25.6–33.6 underline. The reference blur-slide is deliberately replaced by a clean, unblurred calm translation/opacity reveal, matching the caring motion tokens. The seeded variable-width brush and dry-brush holes are preserved. Main headings and benefits remain inside approximately x=72..945, y=150..1550; safety notes sit at y=1600..1720, so posting captions should be kept short or placed to avoid obscuring these notes. Image disclosure is also inside the image window (32px at y989, or y839 in the safe-meal shot), in addition to the footer. All text is selectable code, never generated into photos. Nutrient badges and narration cues derive from the single SHOTS table.

## Asset plan and release
One six-panel photorealistic contact sheet: mother/meal, cooked salmon, hard-boiled eggs, cooked greens, cooked beef, pasteurized milk/yogurt. Each crop is a distinct image region referenced in CSS; no misleading simulated cooking actions. No external real people or private data. Safety and visual direction internally checked; storyboard released for autonomous production.

Validation: inspect styleframe; two stills per scene; full render with audio and without music; extract rendered frames and contact sheet, ffprobe codecs/duration/resolution, audio peak check, independent clean-context final review. Provide project, script/subtitles, asset provenance and limitations. Start editable workbench and verify its imported composition parity.
