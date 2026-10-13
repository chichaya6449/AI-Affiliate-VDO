# Warehouse Affiliate Review Gem — Design Specification

Date: 2026-10-11  
Status: Approved and implemented; revised with opt-in adult scale demonstration and objects-only flood-preparedness wording

## 1. Purpose

Create a reusable Gemini Gem that converts product information and 2–5 reference images into copy-ready prompts for Google Flow and captions for Facebook Page and Shopee Video.

The Gem does not connect to Google Flow, generate images, generate videos, spend Flow credits, download files, or automate a browser. The user manually copies the generated prompts into Google Flow.

The initial product category is household and multipurpose household-utility products. The default creative format is a clean warehouse product-review scene showing only a woman's hands. An explicit opt-in exception may show one fully clothed adult already seated inside an empty large product on a dry floor as a scale reference, while the off-camera reviewer points from the edge of frame. The final Flow video targets Gemini Omni Flash 1.1 in Frames to Video: First mode, vertical 9:16, 10 seconds, with audio enabled and a natural Thai female warehouse-seller voice.

## 2. Success Criteria

The Gem is successful when it:

1. Separates product-reference images from price and promotion images.
2. Extracts product facts without inventing unreadable or unsupported details.
3. Requires explicit user confirmation before producing final prompts and captions.
4. Produces exactly four copy-ready code blocks after confirmation.
5. Makes product identity and packaging fidelity the highest visual priority.
6. Creates a visually strong first-frame prompt with one short Thai hook.
7. Creates an energetic but physically plausible 10-second video prompt that adds no new on-screen text.
8. Produces Thai dialogue that is easy for a video model to pronounce.
9. Produces a Facebook caption and hashtags in one block.
10. Produces a Shopee Video caption and hashtags in one block totaling no more than 150 characters.

## 3. Supported Inputs

Each run handles exactly one household product or one confirmed variant. The user should provide:

- Two to five images per product.
- At least two useful product-view images showing the front, back, side, packaging, included components, or important details.
- An optional price or promotion image.
- Product name, selling point, price, and promotion when available.

Price or promotion images do not count toward the two-product-image minimum. If uploads contain multiple products, multiple unconfirmed variants, more than five images, or a non-household product, the Gem pauses and asks the user to select one supported product, one variant, and the permitted image set.

The Gem may infer ordinary visible attributes such as color, material appearance, component count, and apparent use. It must not infer hidden construction, technical specifications, health claims, durability claims, compatibility, dimensions, warranty, certification, or promotion terms that are not verified under §5.

## 4. Interaction States and Two-Round Flow

The interaction has three explicit states:

- `NEEDS_INPUT`: One or more blocking uncertainties remain. Return the populated portions of the confirmation sheet, identify every blocking field, ask only the highest-priority question, and do not invite confirmation. The token `ยืนยัน` cannot advance this state.
- `AWAITING_CONFIRMATION`: All required uncertainties are resolved, or the user explicitly instructs the Gem to omit an optional price or promotion. Return the complete confirmation sheet and invite confirmation.
- `FINAL`: Entered only from `AWAITING_CONFIRMATION` after valid confirmation. Return the final output contract.

### Round 1: Extract and Confirm

The Gem analyzes the submitted material and responds only with a confirmation sheet containing:

- Current state: `NEEDS_INPUT` or `AWAITING_CONFIRMATION`
- Image-role map using upload order or filename
- Product category
- Product name
- Visible design, color, material, and components
- Demonstrable use
- Verified selling points
- Regular price
- Promotional price
- Discount or promotion
- Promotion conditions
- Information that is unreadable, conflicting, or missing
- Proposed action for the 10-second demonstration
- Proposed reviewer-hand action and, for an adult scale demonstration, two or three exact seated-model gestures
- Camera behavior plus exact start framing, focal target, and final hero framing
- Proposed Thai hook

The image-role map must identify:

- The identity-master image used to control the front/package appearance.
- Supporting product-detail images.
- Data-only price or promotion images that must not be attached to either Flow generation step.

Every confirmation field must contain a value. Use `ไม่ระบุ`, `ไม่มีโปรโมชั่น`, `อ่านไม่ชัด`, or `ขัดแย้ง` as applicable. Claims, prices, and promotions include a short source marker such as `จากผู้ใช้`, `จากรูป 2`, or `จากทั้งสองแหล่ง`.

When the state is `AWAITING_CONFIRMATION`, the response ends by asking the user to reply with the exact word `ยืนยัน` or provide corrections. When the state is `NEEDS_INPUT`, it asks one blocking question and does not invite confirmation.

The Gem must not produce Flow prompts or platform captions during Round 1.

If the user provides corrections, the Gem returns a revised confirmation sheet and waits again. Trim leading and trailing whitespace before evaluating the confirmation token. Only a message whose entire remaining content is exactly `ยืนยัน` authorizes Round 2, and only from `AWAITING_CONFIRMATION`. Punctuation, quotations, additional words, a message containing both confirmation and corrections, and casual acknowledgements such as `โอเค`, `ได้`, `เอาแบบนี้`, or `ยืนยันค่ะ` do not authorize final generation.

### Round 2: Final Output

After explicit confirmation, the Gem returns four labeled code blocks and no checklist or lengthy explanation:

1. `FLOW IMAGE PROMPT`
2. `FLOW VIDEO PROMPT — 10 SECONDS + THAI VOICEOVER`
3. `FACEBOOK PAGE CAPTION + HASHTAGS`
4. `SHOPEE VIDEO CAPTION + HASHTAGS`

The final response contains exactly four Markdown headings, each immediately followed by exactly one fenced code block opened with ` ```text ` (without the surrounding spaces), in the order above. The `text` language tag is required to encourage Gemini's interface to render a per-block copy control. Headings remain outside the fences. The video prompt and Thai voiceover are in the same block. No other prose is permitted except one metadata line immediately after block 4: `จำนวนอักขระ: N/150`. Thus the response has exactly four fenced code blocks; the count line is not a fifth artifact.

After `FINAL`, re-evaluate every change to a fact, claim, price, promotion, hook basis, or demonstration against all validation rules. Enter `NEEDS_INPUT` if the change introduces a blocker; otherwise enter `AWAITING_CONFIRMATION` with a revised confirmation sheet. A copy-only change that does not alter confirmed facts may regenerate the final response directly, but it must return all four blocks and recalculate the Shopee count.

## 5. Reference-Image Routing

The Gem classifies uploaded images into two roles and exposes the mapping in the Round 1 confirmation sheet.

### Product Visual References

These images control:

- Shape and proportions
- Color and visible materials
- Surface finish and patterns
- Logo position
- Label and packaging layout
- Buttons, handles, openings, lids, and attachments
- Number of parts and included accessories

### Price and Promotion References

These images are data sources only. They must not be described as visual references in the Flow prompt because promotional overlays could contaminate the product design or scene. They must not be attached to either Flow generation step.

If one upload contains both a usable product view and promotional overlays, treat it as data-only unless the product can be cleanly isolated without using the overlay design as a visual reference. Flag uncertain mixed-role routing during Round 1.

If multiple images disagree about color, package version, quantity, price, or promotion, the Gem must flag the conflict during Round 1 instead of choosing silently.

`Verified` means clearly visible in a supplied reference or explicitly supplied by the user, provided it is not a restricted claim requiring evidence. If no verified function exists, the Gem may propose a detail-only presentation based on a visible feature. If no verified benefit exists, it asks for a supported selling point or proposes a neutral visible-feature hook for confirmation. Missing function evidence is blocking only when the proposed demonstration depends on that function.

Restricted claims are health, safety, durability, compatibility, warranty, certification, technical-specification, and exact-dimension claims. A user assertion alone does not verify them. They require legible packaging, manufacturer documentation supplied in the conversation, or another explicitly identified authoritative source. Without such evidence, omit the claim or enter `NEEDS_INPUT` when the requested creative depends on it.

## 6. Flow Image Prompt Requirements

The image prompt creates a compelling 9:16 first frame for an affiliate product review. Visual directions are written in concise English. It begins with a compact reference binding that names the identity master and supporting detail images by upload order or filename and states that price/promotion images are data-only and must not be attached as visual ingredients.

Required visual direction:

- Clean warehouse packing-table environment.
- Subtle shelves, parcels, or warehouse context in the background.
- A close 45-degree tabletop view.
- Exactly one pair of adult feminine hands belonging to one off-camera person enters from the lower frame edge and is cropped at the wrists or lower forearms.
- No face, head, torso, full person, or skin above the lower forearms is visible.
- Clean hands, short natural nails, and no visually dominant jewelry.
- The front/primary product face remains unobstructed and occupies approximately 55–65 percent of the frame.
- Bright commercial lighting, good depth, and strong subject separation.
- The composition feels energetic and scroll-stopping rather than static.
- The hands hold or begin to demonstrate the product in a plausible way.

### Adult Scale-Demonstration Exception

The hands-only format remains the default. When the user explicitly requests a person inside a large product and confirms the exception during Round 1, block 1 may instead show exactly one fully clothed adult already seated inside the dry product on a level warehouse floor. The reviewer remains off-camera; only one pointing hand or lower forearm enters from a frame edge. The seated adult may show two anatomically correct hands when the confirmed gesture requires them. No child, additional person, duplicated or anatomically impossible extra hand or limb, climbing, standing, bouncing, rocking, lifting, water, floating, rescue, or human transport is shown. The seated adult is a visual scale reference only and is not evidence of load capacity, safe seating, endorsement, or manufacturer approval. The adult remains seated throughout the video but may use two or three restrained natural presentation gestures to keep the scale demonstration lively.

Product fidelity overrides beauty, drama, and creativity. The prompt must explicitly preserve the exact visible product shape, physical proportions, colors, materials, surface finish, logo placement, packaging layout, visible text placement, controls, openings, components, and accessories. It must prohibit redesigning, simplifying, beautifying, recoloring, relabeling, duplicating, or adding features. Framing distance may change, but physical proportions may not.

The prompt must not invent distinctive details for an unseen side of the product.

### Thai Hook

The image includes exactly one Thai hook:

- Three to seven words.
- Derived only from a verified selling point.
- Readable in approximately one second.
- Large, bold, high-contrast, and located in the upper area of the frame.
- Kept clear of the product, hands, logo, and important details.
- Not a price, discount, unverifiable superlative, or unsupported claim.

For this specification, hook units are the space-separated terms displayed in the hook. The final hook contains three to seven such units and has no punctuation-only unit. The image prompt quotes the exact approved hook and requests exactly one added overlay using that spelling in a bold, high-contrast Thai sans-serif style.

Apart from this specified hook and text already printed on the real product or packaging, the prompt must prohibit all additional text, captions, price tags, promotion graphics, badges, watermarks, and invented logos. Unreadable product copy must not be transcribed or reconstructed; the prompt instructs Flow to preserve its visual appearance, placement, and layout from the reference.

## 7. Flow Video Prompt and Voiceover Requirements

The second block contains the complete Flow video prompt and embedded Thai dialogue. Visual directions are written in concise English. The Thai dialogue appears exactly once under the literal field `Thai voiceover:`. The block contains no explanatory notes, alternatives, or placeholders.

The block begins with these required Flow settings:

- Model: Gemini Omni Flash 1.1
- Mode: Frames to Video: First
- Aspect ratio: 9:16
- Duration: 10 seconds
- Audio: enabled
- Starting image: the approved image generated from block 1

### Video Format

- Vertical 9:16.
- Exactly 10 seconds.
- One continuous shot.
- Warehouse setting and the people mode confirmed in Round 1.
- No cuts, scene changes, unconfirmed people, duplicated or anatomically impossible extra hands or limbs, or additional products.

### Motion and Presentation

The video must feel lively, purposeful, and commercially appealing without becoming chaotic. Product fidelity permits one verified reviewer-hand action and at most one camera behavior. In `HANDS_ONLY`, the reviewer uses the one confirmed two-hand product action. In `ADULT_SCALE_DEMONSTRATION`, the reviewer's one action is followed by the seated adult's two or three confirmed scale-presentation gestures; these gestures are not additional reviewer-hand actions.

Hands-only timing:

- 0–1.2 seconds: begin exactly from the supplied first frame with a stable, readable product and hook.
- 1.2–7.5 seconds: perform one slow, named, verified hand demonstration or detail presentation.
- 7.5–10 seconds: hands settle into a stable hero view with the primary product face unobstructed.

Adult scale-demonstration timing:

- 0–1.2 seconds: begin from the approved first frame with subtle natural breathing and blinking.
- 1.2–3.5 seconds: the reviewer completes the single pointing or rim-tracing action.
- 3.5–7.5 seconds: the seated adult performs the confirmed gestures one after another.
- 7.5–10 seconds: finish with relaxed hands and a clean product hero view.

The Round 1 confirmation sheet defines an allowed action, seated-model gestures, camera behavior, camera focal path, and viewing range. FINAL uses only these confirmed choices. Every product surface plane used by the confirmed camera path is already visible in block 1. Keep the referenced primary face toward the camera. Do not reveal any surface, feature, or mechanism that is not clearly visible in the approved starting image. If the demonstration requires another side, revise block 1 so that side is visible in the approved first frame or choose a different action. For hands-only videos, use either a locked camera or one very slow push-in across the full clip. For an adult scale demonstration, do not default to a locked camera; use one confirmed slow push-in or one gentle side arc, and use a locked camera only when critical product text cannot otherwise remain readable. The move tells a small visual story: begin with the full product silhouette and seated adult as scale, guide attention to the rim and interior depth, limit any arc to five to eight degrees, and end in a clean three-quarter product hero view without cropping the rim or distorting product proportions. The arc remains inside those already-visible surface planes. The prompt must avoid a person holding the product motionless throughout the entire clip, while also prohibiting wide orbits, fast spinning, random shaking, impossible manipulation, opening an unverified component, morphing, deformation, disappearing objects, extra fingers, and hands covering critical product details.

In the adult scale-demonstration exception, the off-camera reviewer performs one confirmed slow pointing or rim-tracing gesture. The seated adult remains seated and performs two or three confirmed gestures in sequence, selected from a brief natural smile while looking toward the rim, an open-palms size gesture, and lightly touching the rim. The product stays stationary on the dry floor, with no water or cargo. The person never climbs, stands, bounces, rocks, lifts, rides in, or carries the product. Reviewer and model actions are staged rather than performed chaotically at the same time.

Adult-scale timing begins with subtle breathing and blinking, moves to the reviewer's single pointing action, then gives the seated adult a short presentation beat, and ends in a relaxed hero view. This replaces any instruction to freeze the seated adult for the whole clip.

### Flood-Preparedness Wording

The word `น้ำท่วม` is not prohibited by itself. For a visibly large container, the Gem may use neutral, objects-only household-preparedness wording such as `มีติดบ้านไว้ใส่ของช่วงน้ำท่วม` when the user requests it. This is an idea for storing or moving belongings, not a claim of watertightness, buoyancy, flood safety, rescue capability, or human transport. Generated scenes remain dry and never show floating, floodwater, or a person being transported. Wording such as `ใช้แทนเรือ`, `ลอยน้ำได้`, `ขนคนได้`, and `ปลอดภัยในน้ำท่วม` is prohibited without authoritative evidence and remains outside this exception.

### Text Preservation

The video prompt must instruct Flow not to intentionally add or rewrite text. Keep the text-bearing product face front-facing, fully visible, and as stable as the verified action permits. Preserve the approved first-frame hook without intentional rewriting, translation, duplication, animation, movement, or replacement. Require exact spelling only for strings confirmed as legible in Round 1; preserve the appearance and layout of unreadable printed areas without reconstructing them. The prompt must not create subtitles, prices, promotion graphics, badges, or a visual CTA. These are prompt-level safeguards, not a guarantee that Flow will render every glyph without distortion.

### Thai Voice

Immediately before `Thai voiceover:`, the video prompt includes a `Voice performance:` direction. The off-screen adult Thai woman sounds cheerful, warm, energetic, and credible, with an audible smile, lively pitch variation, and natural conversational rhythm. She emphasizes the hook, primary benefit, verified offer, and final CTA when present. The delivery is clear rather than rushed and is never flat, monotone, robotic, shouted, artificially overexcited, or styled like a formal announcer. No speaker is visible, there is no lip-sync or second voice, and the spoken words never appear as subtitles.

The 10-second dialogue should follow this intent:

- Short hook
- One primary verified benefit or demonstration
- Verified price or promotion when useful and confirmed
- End exactly with: `กดตะกร้าด้านล่างได้เลยค่ะ`

The final CTA may be preceded by a short natural lead-in, but after trimming terminal punctuation the dialogue must end exactly with `กดตะกร้าด้านล่างได้เลยค่ะ`, appearing once, with nothing spoken after it.

The dialogue contains one or two short sentences, at most two deliberate pause points, begins at approximately 0.5 seconds, and finishes by 9.0–9.5 seconds at a natural conversational pace without speeding up. It uses only one primary spoken benefit and reserves two brief breathing beats for expressive pitch and emphasis; secondary benefits stay in the hook or captions. Target no more than 82 Unicode code points for the exact spoken line, including spaces and the mandatory CTA but excluding surrounding quotation marks. When target-voice synthesis is available, timing passes only when measured at no more than 9.0 seconds at normal expressive speed with those pauses intact. When synthesis is unavailable, 90 Unicode code points is the absolute fallback maximum, but 82 or fewer remains preferred. If verified promotion conditions make the line too long, remove a secondary claim first, then omit the promotion from speech before shortening the verified primary benefit or mandatory CTA. Audio is a dominant clean close-mic voice with subtle warehouse room tone and no lyric music masking speech.

## 8. AI-Safe Thai Speech Normalization

Before returning the final video prompt, the Gem must normalize the dialogue for reliable AI pronunciation.

Rules:

- Do not use the repetition mark `ๆ`; repeat the spoken word instead.
- Convert numerals used in speech to Thai words.
- Convert `%` to the spoken word `เปอร์เซ็นต์` while preserving the promotion meaning.
- Convert `1+1` to `ซื้อหนึ่งแถมหนึ่ง` only when that exact offer mechanic is verified.
- Convert price shorthand such as `129.-` to `หนึ่งร้อยยี่สิบเก้าบาท`.
- Spell out units and common abbreviations.
- Replace symbols such as `/`, `+`, `&`, and `%` according to their confirmed meaning, never through blind substitution.
- Use Thai phonetic spelling for an English brand name only in the dialogue; do not modify the brand spelling in visual product instructions or captions.
- Avoid parentheses, hashtags, emojis, URLs, and dense punctuation in dialogue.
- Use short phrases with natural pause points.
- Avoid tongue-twisting alliteration and ambiguous number grouping.
- Convert decimals, ranges, dimensions, quantities, and units contextually: for example `1.5 ลิตร` becomes `หนึ่งจุดห้าลิตร`, `1–2 ชิ้น` becomes `หนึ่งถึงสองชิ้น`, and `30 × 40 ซม.` becomes `สามสิบคูณสี่สิบเซนติเมตร`.
- Confirm or omit an alphanumeric model or unclear English-brand pronunciation rather than guessing.
- After normalization, compare the spoken price, quantity, unit, promotion, and conditions with the confirmed facts to ensure semantic equivalence.
- Keep the script within the timing or deterministic character budget defined above.

Example transformation:

`ลด 20% ราคา 129.-` becomes `ลดลงยี่สิบเปอร์เซ็นต์ เหลือหนึ่งร้อยยี่สิบเก้าบาทค่ะ`, but only when both the percentage and discounted-price relationship are confirmed.

## 9. Promotion Semantics

Every prompt and caption must preserve the material meaning of confirmed offer qualifiers, including `เริ่มต้น`, `สูงสุด`, `เมื่อใช้โค้ด`, minimum spend, eligible variant, quantity, sales channel, membership requirement, and validity dates.

- Use `เหลือ…บาท`, `จาก…เหลือ…`, or `ลด…เปอร์เซ็นต์` only when the relationship is explicitly confirmed.
- If only one price is known, say `ราคา…บาท`; never imply a discount.
- Do not convert `N+M` into `ซื้อ N แถม M` unless the offer mechanics are verified.
- Do not say `วันนี้`, `ตอนนี้`, `รีบ`, `ใกล้หมด`, or imply current availability unless verified.
- If the displayed percentage conflicts with the price arithmetic, stop in Round 1 instead of selecting either value.
- A clearly expired promotion is marked `หมดอายุ` and omitted from all final artifacts without blocking. A promotion whose current validity cannot be established enters `NEEDS_INPUT`; ask whether to omit it or request valid dates. It may reach `AWAITING_CONFIRMATION` only after one of those resolutions.
- Shortened Facebook, Shopee, or voiceover wording must retain all material conditions; if they do not fit, omit the promotion entirely.

## 10. Facebook Page Caption and Hashtags

The third code block contains both the Facebook caption and hashtags.

Requirements:

- Caption prose must be Thai. Preserve confirmed brand and model spellings in their original script. Hashtags may use Thai or the confirmed original brand spelling.
- Use this order: truthful hook; household problem plus one verified benefit; optional verified price/promotion paragraph with every material condition; shopping CTA; final hashtag line.
- Use short paragraphs that are easy to scan.
- Include a user-supplied link only when provided; never invent one.
- Do not invent product claims, urgency, stock levels, free shipping, discounts, or promotion deadlines.
- Do not use unsupported superlatives such as `ดีที่สุด`, `ถูกที่สุด`, or `ขายดีอันดับหนึ่ง` in prose or hashtags.
- Include exactly three to six distinct, relevant hashtags on the final line.
- Keep hashtags in the same code block as the caption and never intersperse them with prose.

## 11. Shopee Video Caption and Hashtags

The fourth code block contains the complete Shopee Video caption and hashtags.

The combined content must be one line and must not exceed 150 characters. Caption prose must be Thai; confirmed brand and model spellings may remain in their original script. Target no more than 145 to provide a platform-counting safety margin. Normalize the logical payload to Unicode NFC before validation, then require no internal line break and no leading or trailing whitespace. The payload is the single logical text line between the fences; exactly one structural LF or CRLF immediately before the closing fence is not payload and is removed before counting. Any additional outer whitespace or additional line break is invalid. Count the exact logical payload excluding the heading and fence syntax. Calculate both Unicode code points and UTF-16 code units; define `N` as the larger count. Thai base letters, vowels, tone marks, spaces, punctuation, `#`, hashtag letters, emoji components, and variation selectors all count. Prefer no emoji because emoji frequently occupy multiple UTF-16 units.

The Gem must:

- Prioritize the product name, primary benefit, verified offer, CTA, and the most useful hashtags.
- Include at least one complete, relevant hashtag. Remove secondary hashtags first but never delete the final hashtag.
- Remove secondary wording and secondary hashtags first when shortening.
- Never truncate a word, price, promotion, or hashtag midway.
- Avoid URLs.
- Report `จำนวนอักขระ: N/150` outside the code block.
- Generate `N` from the final exact payload, never by estimation, and do not silently trim or normalize after counting.
- Recalculate the count after every revision. If shortening is required, remove complete secondary phrases or hashtags and count again.

## 12. Manual Flow Handoff

The Round 1 image-role map tells the user which references to use. The final prompts assume this manual sequence:

1. Attach only the confirmed product visual references to Flow and use block 1 to create the 9:16 first frame.
2. Do not attach price or promotion images to Flow.
3. Review the generated first frame manually for product fidelity and hook spelling.
4. Use the approved generated first frame as the starting image for block 2.
5. In Flow, select Gemini Omni Flash 1.1, Frames to Video: First, 9:16, 10 seconds, with audio enabled.

The Gem writes instructions and cannot guarantee that Flow will render exact text, anatomy, duration, or product fidelity. Acceptance evaluates prompt compliance, not rendered-media compliance.

## 13. Error and Ambiguity Handling

The Gem must pause during Round 1 when:

- Product images appear to show different variants.
- The price or promotion cannot be read confidently.
- The supplied price conflicts with an image.
- The proposed demonstration depends on a function that cannot be verified, and no confirmed detail-only presentation has been selected.
- A requested claim is not supported.
- Fewer than two useful product images are available.

It should ask only the minimum question needed to resolve the uncertainty. It must not conceal uncertainty or fill gaps creatively. An unreadable optional promotion may be resolved when the user explicitly says to omit the promotion. Unreadable product text is blocking only when needed to establish product identity, a claim, price, or promotion.

## 14. Out of Scope

The first version does not:

- Generate images or videos.
- Connect to or control Google Flow.
- Spend or monitor Flow credits.
- Download media.
- Create multiple creative variants.
- Produce separate voiceover and video-prompt blocks.
- Produce a manual Flow checklist.
- Show the reviewer's face or body; only the explicit adult scale-reference exception may show one other adult.
- Show children, water, floating, rescue, or human transport in the adult scale-reference exception.
- Add captions, subtitles, prices, promotion graphics, or visual CTA text during video generation.

## 15. Acceptance Tests

The finished Gem instructions will be tested with at least these cases:

1. A household product with clear multi-angle references and no promotion.
2. A household product with a clear regular price, promotional price, and percentage discount.
3. Conflicting prices across two uploaded images.
4. A blurry promotion image that must trigger clarification.
5. A product whose function cannot be inferred safely proposes a detail-only presentation; it enters `NEEDS_INPUT` only when the user requests a function-dependent demonstration.
6. Dialogue containing a percentage, price, quantity, English brand, and unit.
7. A Shopee result initially exceeding 150 characters that must be shortened and recounted.
8. A product image containing existing packaging text plus one requested hook, ensuring no additional text is requested.
9. `โอเค`, `ยืนยันค่ะ`, `ยืนยัน` plus a correction, and bare `ยืนยัน` during `NEEDS_INPUT` do not advance.
10. Bare `ยืนยัน` advances only from `AWAITING_CONFIRMATION`.
11. One product image plus one promotion image is rejected as insufficient product coverage.
12. An unreadable optional promotion can be resolved by explicitly omitting the promotion.
13. Mixed-role images, multiple products, and unconfirmed variants trigger clarification.
14. A post-final factual correction returns to confirmation; a copy-only revision returns all four blocks and a recalculated count.
15. Final output has exactly four fences, headings outside fences, and only the permitted count line.
16. Hook unit counting follows the space-separated-unit rule.
17. Shopee validation checks Unicode code points and UTF-16 units, rejects line breaks and outer whitespace, and reports the larger exact count.
18. The required CTA appears exactly once as the final spoken phrase.
19. `129 บาท` without a former price produces no `เหลือ`, `จาก`, or `ลด` wording.
20. `เริ่มต้น 99 บาท` and `ลดสูงสุด 50%` retain their qualifiers everywhere.
21. A code-dependent or minimum-spend price is never stated without all material conditions.
22. Conflicting price arithmetic and displayed percentage returns to `NEEDS_INPUT`.
23. A 150-count Shopee payload passes and a 151-count payload fails under the conservative counting rule.
24. Shopee payloads represented as `payload`, `payload\n`, and `payload\r\n` by a renderer produce the same `N`; `payload ` and `payload\n\n` fail.
25. A Shopee payload with no complete hashtag fails; one complete relevant hashtag passes; a truncated hashtag fails.
26. Facebook and Shopee caption prose is Thai while confirmed brand/model spelling may remain in its original script.
27. A clearly expired promotion is omitted without blocking; an uncertain validity date enters `NEEDS_INPUT` until omitted or resolved.
28. An explicit adult scale-demonstration request uses one pointing reviewer hand and one fully clothed seated adult in an empty product on a dry floor, with no load-capacity or safety claim.
29. Objects-only flood-preparedness wording may mention keeping the product at home to hold belongings during flooding, while boat, flotation, rescue, and human-transport claims remain prohibited.

The final response passes only when it contains exactly four correctly labeled code blocks, the embedded dialogue uses AI-safe Thai and fits the defined timing or proxy budget, and the Shopee block is verified at no more than 150 characters under the conservative counting rule.
