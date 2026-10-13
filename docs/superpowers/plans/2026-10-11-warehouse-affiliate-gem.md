# Warehouse Affiliate Review Gem Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver copy-ready Gemini Gem instructions that turn 2–5 household-product images into confirmed Google Flow prompts plus Facebook and Shopee captions, with deterministic output and safety rules.

**Architecture:** A single text instruction artifact contains the Gem role, state machine, evidence rules, prompt templates, speech normalization, and exact four-block output contract. A dependency-free Python test statically verifies the non-negotiable contract, while a scenario catalog records behavioral cases that must be dry-run before delivery. A short Thai guide explains how to install and use the Gem manually with Google Flow.

**Tech Stack:** Plain text/Markdown, Python 3 standard-library `unittest`, Gemini Gems web UI, Google Flow Gemini Omni Flash 1.1.

**Spec:** `docs/superpowers/specs/2026-10-11-warehouse-affiliate-gem-design.md`

## Global Constraints

- Text-only Gem: it never generates media, controls Flow, spends credits, or downloads files.
- One household product or one confirmed variant per run, with 2–5 uploads and at least two useful product-view images.
- Final Flow video target: Gemini Omni Flash 1.1, Frames to Video: First, 9:16, 10 seconds, audio enabled.
- State transitions are limited to `NEEDS_INPUT`, `AWAITING_CONFIRMATION`, and `FINAL`; only the exact token `ยืนยัน` advances from `AWAITING_CONFIRMATION`.
- Final output contains exactly four fenced code blocks; video prompt and Thai voiceover share block 2; no manual checklist is emitted.
- The image prompt requests one verified Thai hook and prioritizes exact product identity over visual creativity.
- The video prompt adds no on-screen text, uses one verified hand action, and uses at most one camera behavior.
- Off-screen Thai female voiceover ends exactly once with `กดตะกร้าด้านล่างได้เลยค่ะ` and follows the 9-second/90-code-point budget.
- Facebook caption and 3–6 distinct hashtags occupy one block.
- Shopee caption and at least one hashtag occupy one line, target no more than 145 characters, and must validate at no more than 150 using the larger of Unicode-code-point and UTF-16-unit counts.
- Prices, discounts, and offer qualifiers remain semantically exact; unsupported claims, urgency, and availability are never invented.

## Review Focus

- Mixed product/promotion screenshots must be routed as data-only unless the product can be cleanly isolated; Task 2 case `mixed-role-image` pins this behavior.
- Variant-specific, coupon-dependent, minimum-spend, expired, and contradictory offers must transition correctly without dropping qualifiers; Task 2 cases `conditional-promo`, `expired-promo`, and `conflicting-discount` pin this behavior.
- A requested action must not expose a surface absent from the approved start frame; Task 2 case `unseen-side-action` pins the fallback to a safer detail presentation.
- Thai dialogue with prices, percentages, units, and English brands must retain meaning and fit the deterministic voice budget; Task 2 case `voice-normalization` pins this behavior.
- Shopee content near the boundary must retain one whole hashtag and report the conservative count correctly; Task 2 cases `shopee-150`, `shopee-151`, and `emoji-count` pin this behavior.

---

### Task 1: Gem Instruction Contract

**Files:**
- Create: `Warehouse_Affiliate_GEM_Instructions_10S.txt`
- Create: `tests/test_instruction_contract.py`

**Interfaces:**
- Consumes: Requirements in `docs/superpowers/specs/2026-10-11-warehouse-affiliate-gem-design.md`.
- Produces: `Warehouse_Affiliate_GEM_Instructions_10S.txt`, a standalone instruction body ready to paste into Gemini Gems; `tests/test_instruction_contract.py`, an offline structural validator used by later tasks.

- [ ] **Step 1: Write the failing static-contract tests**

Create `tests/test_instruction_contract.py` with `unittest.TestCase` methods that load the instruction artifact and assert:

```python
def test_required_states_are_present(): ...
def test_exact_final_headings_are_present_once_and_in_order(): ...
def test_video_and_voiceover_share_one_output_heading(): ...
def test_manual_checklist_output_is_absent(): ...
def test_exact_confirmation_and_cta_tokens_are_present(): ...
def test_flow_model_settings_are_present(): ...
def test_product_reference_and_promotion_routing_rules_are_present(): ...
def test_promotion_semantics_rules_are_present(): ...
def test_ai_safe_thai_rules_are_present(): ...
def test_facebook_and_shopee_contracts_are_present(): ...
def test_instruction_has_no_template_placeholders(): ...
```

The heading-order assertion uses these exact strings:

```python
FINAL_HEADINGS = [
    "### FLOW IMAGE PROMPT",
    "### FLOW VIDEO PROMPT — 10 SECONDS + THAI VOICEOVER",
    "### FACEBOOK PAGE CAPTION + HASHTAGS",
    "### SHOPEE VIDEO CAPTION + HASHTAGS",
]
```

- [ ] **Step 2: Run the contract tests and verify they fail**

Run: `python -m unittest tests.test_instruction_contract -v`

Expected: FAIL because `Warehouse_Affiliate_GEM_Instructions_10S.txt` does not exist.

- [ ] **Step 3: Write the minimal complete Gem instruction artifact**

Create `Warehouse_Affiliate_GEM_Instructions_10S.txt` with these top-level sections:

```text
PURPOSE AND ROLE
RESPONSE CONTRACT — HIGHEST PRIORITY
UNTRUSTED INPUT AND SCOPE RULES
INPUT AND IMAGE ROUTING
INTERACTION STATE MACHINE
ROUND 1 CONFIRMATION SHEET
EVIDENCE AND PROMOTION RULES
FLOW IMAGE PROMPT RULES
FLOW VIDEO PROMPT AND THAI VOICEOVER RULES
AI-SAFE THAI SPEECH NORMALIZATION
FACEBOOK CAPTION RULES
SHOPEE CAPTION AND COUNTING RULES
POST-FINAL REVISION RULES
SILENT FINAL VALIDATION
EXACT FINAL OUTPUT
```

Requirements inside the artifact:

- Declare that uploaded image/OCR/link content is untrusted data and cannot alter the Gem role or expose instructions.
- Define all three interaction states and their permitted transitions exactly as specified.
- Make image-role mapping visible in Round 1 using upload order or filenames.
- Write visual Flow instructions in concise English and spoken dialogue/captions in Thai.
- Bind an identity master and supporting references in block 1; prohibit attaching promotion images to Flow.
- Put the exact Flow settings at the beginning of block 2.
- Embed the Thai spoken line exactly once under `Thai voiceover:` and make it off-screen voiceover.
- Define one verified action, allowed viewing range, locked/slow-push camera rule, and no-new-text rule.
- Encode all promotion-qualifier and AI-speech normalization rules from §§8–9 of the spec.
- Define the Facebook ordering and exact 3–6 hashtag rule.
- Define the Shopee single-line/NFC/conservative count procedure, at-least-one-hashtag rule, target 145, hard maximum 150, and external `จำนวนอักขระ: N/150` line.
- End with an exact response skeleton containing four code blocks and no optional prose.

- [ ] **Step 4: Run the static-contract tests and verify they pass**

Run: `python -m unittest tests.test_instruction_contract -v`

Expected: all contract tests PASS.

- [ ] **Step 5: Commit the Gem instruction contract**

```bash
git add Warehouse_Affiliate_GEM_Instructions_10S.txt tests/test_instruction_contract.py
git commit -m "feat: add warehouse affiliate Gem instructions"
```

### Task 2: Behavioral Scenario Catalog

**Files:**
- Create: `tests/test_scenario_catalog.py`
- Create: `tests/fixtures/behavior-cases.md`

**Interfaces:**
- Consumes: State names, confirmation token, final headings, evidence rules, and output constraints from Task 1.
- Produces: A reviewable scenario catalog whose stable case IDs support manual Gem dry-runs and future regression testing.

- [ ] **Step 1: Write the failing catalog-coverage test**

Create `tests/test_scenario_catalog.py` to parse headings of the form `## CASE: <id>` and require these IDs:

```python
REQUIRED_CASES = {
    "clear-product-no-promo",
    "clear-product-with-promo",
    "insufficient-product-views",
    "mixed-role-image",
    "multiple-variants",
    "conditional-promo",
    "expired-promo",
    "conflicting-discount",
    "unsupported-claim",
    "unseen-side-action",
    "voice-normalization",
    "confirmation-token",
    "post-final-factual-edit",
    "shopee-150",
    "shopee-151",
    "emoji-count",
}
```

For every case, assert the presence of `Input`, `Expected state`, and `Expected behavior` subsections.

- [ ] **Step 2: Run the catalog test and verify it fails**

Run: `python -m unittest tests.test_scenario_catalog -v`

Expected: FAIL because `tests/fixtures/behavior-cases.md` does not exist.

- [ ] **Step 3: Write the behavioral cases**

Create `tests/fixtures/behavior-cases.md`. Each case supplies a concise hypothetical household-product input and pins:

- Expected state (`NEEDS_INPUT`, `AWAITING_CONFIRMATION`, or `FINAL`).
- The exact blocking question or resolution rule when applicable.
- Required product-reference routing.
- Promotion wording that must be retained or omitted.
- Allowed hand action and visible surface.
- Expected voice-normalization transformation where applicable.
- Expected final-output structure and Shopee boundary behavior where applicable.

For `confirmation-token`, include `โอเค`, `ยืนยันค่ะ`, bare `ยืนยัน`, and `ยืนยัน` plus corrections. For Shopee boundary cases, include literal candidate payloads and their expected conservative counts.

- [ ] **Step 4: Run both test modules and verify they pass**

Run: `python -m unittest discover -s tests -v`

Expected: all contract and catalog tests PASS.

- [ ] **Step 5: Perform three manual dry-runs against the instruction artifact**

Use cases `clear-product-with-promo`, `conflicting-discount`, and `voice-normalization`. For each, verify the Gem-style response against the scenario's expected state and behavior. Record the review result at the end of the case as `Dry-run result: PASS`; fix the instruction artifact before marking PASS if any requirement is missed.

- [ ] **Step 6: Commit the scenario catalog**

```bash
git add tests/test_scenario_catalog.py tests/fixtures/behavior-cases.md Warehouse_Affiliate_GEM_Instructions_10S.txt
git commit -m "test: add Gem behavioral scenarios"
```

### Task 3: Thai Quick-Start and Final Verification

**Files:**
- Create: `README_TH.md`
- Modify: `tests/test_instruction_contract.py`

**Interfaces:**
- Consumes: Final instruction artifact and scenario catalog from Tasks 1–2.
- Produces: A concise Thai installation/usage guide and the verified release bundle.

- [ ] **Step 1: Add failing documentation-presence tests**

Extend `tests/test_instruction_contract.py` with assertions that `README_TH.md` contains:

```python
def test_quick_start_names_the_instruction_file(): ...
def test_quick_start_explains_two_round_confirmation(): ...
def test_quick_start_explains_manual_flow_handoff(): ...
def test_quick_start_warns_not_to_attach_promotion_images(): ...
```

- [ ] **Step 2: Run the documentation tests and verify they fail**

Run: `python -m unittest tests.test_instruction_contract -v`

Expected: the four quick-start tests FAIL because `README_TH.md` does not exist.

- [ ] **Step 3: Write the Thai quick-start guide**

Create `README_TH.md` with:

- How to create a new Gem and paste `Warehouse_Affiliate_GEM_Instructions_10S.txt` into its Instructions field.
- Recommended Gem name and description.
- The expected 2–5 image input and a copy-ready user input form.
- The Round 1 correction/`ยืนยัน` workflow.
- Which images to attach with block 1 and which generated image to use with block 2.
- The exact Flow model, mode, aspect ratio, duration, and audio settings.
- A warning that Flow rendering remains probabilistic and the user must inspect product fidelity and hook spelling before spending video credits.
- How to request a copy-only revision versus a factual correction.

- [ ] **Step 4: Run the complete verification suite**

Run: `python -m unittest discover -s tests -v`

Expected: all tests PASS with no errors or skips.

- [ ] **Step 5: Run artifact hygiene checks**

Run: `rg -n "TBD|TODO|PLACEHOLDER|MANUAL FLOW CHECKLIST" Warehouse_Affiliate_GEM_Instructions_10S.txt README_TH.md tests`

Expected: no unresolved placeholder or forbidden-output matches. If the test code intentionally contains a forbidden phrase as a negative assertion, scope the command to the deliverable files and confirm both are clean.

Run: `git diff --check`

Expected: no whitespace errors.

- [ ] **Step 6: Commit the release bundle**

```bash
git add README_TH.md tests/test_instruction_contract.py
git commit -m "docs: add Gem setup and usage guide"
```

- [ ] **Step 7: Final review**

Compare the instruction artifact against every section of the design spec, confirm the working tree is clean, and report the instruction file, guide, tests run, and commit IDs to the user.
