# โกดังทุบราคา 10S — Behavior Cases

## CASE: single-clear-image

### Input

One clear image shows a single household product, its visible shape, color, logo, and ordinary use. No price is supplied.

### Expected state

FINAL

### Expected behavior

Accept the single image as the identity master and generate all four final blocks without confirmation. Omit unknown price and promotion details instead of asking for them.

## CASE: single-mixed-marketplace-image

### Input

One marketplace screenshot clearly shows a single selected product plus shop UI, badges, and price graphics.

### Expected state

FINAL

### Expected behavior

Use only the clearly isolated product area as identity evidence. Exclude marketplace UI, badges, prices, and unrelated graphics from Flow. Do not request a second image merely because the reference is mixed.

## CASE: multiple-products

### Input

Two uploaded images show different household products and the user has not selected one.

### Expected state

NEEDS_INPUT

### Expected behavior

Ask one concise question requesting the single product to use. Do not output a confirmation sheet or partial prompt.

## CASE: conflicting-required-promotion

### Input

Two supplied promotion sources show different current prices. The user explicitly requires the current promotion in the voiceover.

### Expected state

NEEDS_INPUT

### Expected behavior

Ask one concise question asking which promotion value is authoritative. If the offer were optional, the Gem would omit it and continue.

## CASE: unsupported-optional-claim

### Input

A clear product image is supplied. The user mentions an unsupported waterproof claim as an optional secondary point.

### Expected state

FINAL

### Expected behavior

Omit the unsupported restricted claim and continue with visible ordinary benefits. Do not block when the optional claim can be removed.

## CASE: conditional-promotion

### Input

A legible current offer states a discounted price only when a coupon is collected, for one eligible variant, with a minimum spend and a validity date.

### Expected state

FINAL

### Expected behavior

Use the offer only with every material qualifier intact. If all conditions do not fit a destination limit, omit the complete offer rather than shortening its meaning.

## CASE: expired-promotion

### Input

A promotion card has a clearly readable validity date that ended before the current date.

### Expected state

FINAL

### Expected behavior

Treat the promotion as expired and omit it from Hook, voiceover, Facebook copy, and Shopee copy. Continue using non-promotional product facts without asking a question.

## CASE: latest-user-direction

### Input

After receiving final blocks, the user asks to change the Hook and use a different safe hand demonstration.

### Expected state

FINAL

### Expected behavior

Use the latest valid instruction, apply it immediately, regenerate all four blocks, and do not ask for confirmation.

## CASE: male-hands-default

### Input

One clear product image is supplied with no request for a visible full person.

### Expected state

FINAL

### Expected behavior

Use HANDS_ONLY with the default male gender. If two hands are necessary, show exactly one left hand and one right hand belonging to the same adult man, with natural anatomy and no additional hands or arms.

## CASE: adult-male-explicit

### Input

The user explicitly asks for one fully clothed adult man to stand beside and safely demonstrate a large household product.

### Expected state

FINAL

### Expected behavior

Use ADULT_DEMONSTRATION with the default male gender only because the user explicitly requested a visible person. Show one relevant natural demonstration without additional people or unsafe use.

## CASE: explicit-gender-override

### Input

After the Gem has produced a default male version, the user explicitly requests a woman reviewer and woman narrator instead.

### Expected state

FINAL

### Expected behavior

Apply the change immediately and use the selected gender consistently across hands, visible demonstrator, voice, and CTA. Use the matching polite particle, and do not leave any male-only hand, person, narrator, or CTA instruction in the regenerated blocks.

## CASE: hook-only-added-text

### Input

The product and one verified selling point are clear. The user does not request a price on the image.

### Expected state

FINAL

### Expected behavior

Add exactly one Thai Hook in the upper safe area. Keep no price signage, yellow signs, discount boards, currency symbols, percentages, visual CTA, or other generated text in the image.

## CASE: product-identity-lock

### Input

The approved first frame shows one selected product held in a stable POV pose.

### Expected state

FINAL

### Expected behavior

Begin from the exact first frame and preserve the same product throughout. Allow only subtle supported motion, with no spin or rotation, no morphing, no new side, and no product replacement.

## CASE: male-voice-150-170

### Input

The product has a relatable problem, a verified benefit, and a verified offer. The clip duration is ten seconds.

### Expected state

FINAL

### Expected behavior

Write a problem-led 150–170 character voiceover for an energetic off-screen Thai man. Keep the complete selling progression and end exactly with `กดตะกร้าด้านล่างได้เลยครับ`.

## CASE: shopee-150

### Input

Validate a boundary payload whose body is literal ASCII test data ending in one complete hashtag.

### Expected state

FINAL

### Expected behavior

The payload passes because both conservative counts are exactly 150. Retain the complete hashtag and report 150/150.

Literal payload: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa #x`
Expected conservative count: 150

## CASE: shopee-151

### Input

Validate an over-limit payload whose body is literal ASCII test data ending in one complete hashtag.

### Expected state

FINAL after shortening

### Expected behavior

The original payload fails at 151. Remove a complete secondary unit, retain a complete hashtag, recalculate, and return a payload at or below 150.

Literal payload: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa #x`
Expected conservative count: 151

## CASE: emoji-count

### Input

Validate a short Shopee payload containing one non-BMP emoji.

### Expected state

FINAL

### Expected behavior

Count the normalized payload as 13 Unicode code points and 14 UTF-16 code units, report the larger value 14, and retain the complete hashtag.

Literal payload: `สินค้า🧽 #บ้าน`
Expected conservative count: 14

