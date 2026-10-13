import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_FILE = ROOT / "Warehouse_Affiliate_GEM_Instructions_10S.txt"
README_FILE = ROOT / "README_TH.md"

FINAL_HEADINGS = [
    "### FLOW IMAGE PROMPT",
    "### FLOW VIDEO PROMPT — 10 SECONDS + THAI VOICEOVER",
    "### FACEBOOK PAGE CAPTION + HASHTAGS",
    "### SHOPEE VIDEO CAPTION + HASHTAGS",
]


class InstructionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = INSTRUCTION_FILE.read_text(encoding="utf-8")

    def test_only_needs_input_and_final_are_active_states(self):
        self.assertIn("Use exactly two response states: NEEDS_INPUT or FINAL", self.text)
        self.assertNotIn("only the exact standalone message `ยืนยัน`", self.text)
        self.assertNotIn("ROUND 1 CONFIRMATION SHEET", self.text)

    def test_clear_input_goes_directly_to_final_without_confirmation(self):
        required = (
            "Go directly to FINAL",
            "Do not ask for confirmation",
            "Do not require the user to type `ยืนยัน`",
            "ask only one concise highest-priority question",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_latest_user_direction_is_applied_immediately_within_flow_policy(self):
        required = (
            "LATEST USER DIRECTION",
            "apply it immediately",
            "Do not argue",
            "Flow policy",
            "latest user instruction overrides the defaults",
            "Male voice and male hands are defaults",
            "an explicit later gender request overrides them",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_one_to_five_images_are_supported_and_one_can_be_enough(self):
        required = (
            "one to five uploaded images",
            "One clear product image is sufficient",
            "supporting detail images are optional",
            "Do not block merely because only one image was uploaded",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
        self.assertNotIn("at least two useful product-view images", self.text)

    def test_exact_final_headings_are_present_once_and_in_order(self):
        positions = []
        for heading in FINAL_HEADINGS:
            self.assertEqual(1, self.text.count(heading), heading)
            positions.append(self.text.index(heading))
        self.assertEqual(sorted(positions), positions)

    def test_exact_output_skeleton_uses_four_copyable_text_blocks(self):
        tail = self.text.split("EXACT FINAL OUTPUT", 1)[1]
        skeleton = tail[tail.index(FINAL_HEADINGS[0]):].strip()
        fence_lines = re.findall(r"(?m)^```.*$", skeleton)
        self.assertEqual(["```text", "```"] * 4, fence_lines)
        pattern_parts = []
        for heading in FINAL_HEADINGS:
            pattern_parts.append(re.escape(heading) + r"\n```text\n.+?\n```")
        exact_pattern = r"\A" + r"\n\n".join(pattern_parts) + r"\nจำนวนอักขระ: N/150\Z"
        self.assertRegex(skeleton, re.compile(exact_pattern, re.DOTALL))

    def test_video_and_voiceover_share_one_output_block(self):
        self.assertIn("Thai voiceover:", self.text)
        self.assertNotIn("### THAI VOICEOVER", self.text)
        self.assertNotIn("MANUAL FLOW CHECKLIST", self.text)

    def test_flow_settings_are_present(self):
        for value in (
            "Model: Gemini Omni Flash 1.1",
            "Mode: Frames to Video: First",
            "Aspect ratio: 9:16",
            "Duration: 10 seconds",
            "Audio: enabled",
        ):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_default_scene_is_clean_realistic_thai_clearance_warehouse(self):
        required = (
            "realistic mobile-phone POV",
            "medium-sized Thai clearance warehouse",
            "bright natural daylight",
            "clean and organized",
            "stacks or shelves of the exact same product",
            "vibrant authentic branded packaging",
            "no opaque brown boxes",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_image_has_exactly_one_thai_hook_and_no_price_signage(self):
        required = (
            "exactly one added Thai hook",
            "three to seven space-separated units",
            "upper safe area",
            "NO yellow cardboard signs",
            "NO price signs",
            "no currency symbols",
            "The approved Thai hook is the only added-text exception",
            "The Hook must never be a price or discount",
            "The ban on numbers applies only to newly generated signage",
            "preserve authentic numbers already printed on the real product or packaging",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_expired_and_conditional_promotions_are_handled_safely(self):
        required = (
            "clearly expired promotion",
            "omit it from every final artifact",
            "Preserve every material qualifier",
            "minimum spend",
            "eligible variant",
            "validity date",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_default_hands_are_adult_male_and_anatomically_locked(self):
        required = (
            "HANDS_ONLY",
            "adult man's hands",
            "ONE LEFT HAND and ONE RIGHT HAND",
            "belonging to the SAME single person",
            "no third hand",
            "no extra arm",
            "no detached or floating hand",
            "natural finger count and proportions",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_full_person_is_used_only_on_explicit_request(self):
        required = (
            "ADULT_DEMONSTRATION",
            "only when the user explicitly requests a visible person",
            "Never add a full person automatically",
            "one fully clothed adult man",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_explicit_gender_override_propagates_without_male_only_rules(self):
        required = (
            "use the selected gender consistently",
            "adult man by default",
            "hands, visible demonstrator, voice, and CTA",
            "matching Thai polite particle",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
        self.assertNotIn("confirmed people mode, including adult male identity", self.text)

    def test_product_identity_is_locked_from_first_frame_through_video(self):
        required = (
            "STRICT PRODUCT IDENTITY LOCK",
            "sole visual source of truth",
            "start exactly from the approved initial frame",
            "Never replace, redesign, substitute, morph, swap, duplicate, dissolve",
            "do not spin, rotate, turn around, or float the product",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_video_motion_is_subtle_but_commercially_interesting(self):
        required = (
            "subtle camera motion",
            "one purposeful reviewer-hand demonstration",
            "Repeat the complete applicable anatomy and hand constraints from block one inside block two",
            "consistent from start to finish",
            "commercially engaging rather than stiff",
            "Do not add any new on-screen text",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_voice_is_male_problem_led_and_matches_tested_length(self):
        required = (
            "By default, use one off-screen adult Thai man",
            "150 to 170 Unicode code points",
            "finish the complete line within ten seconds",
            "problem → consequence or desire → product as solution → primary benefit → verified offer when useful → CTA",
            "กดตะกร้าด้านล่างได้เลยครับ",
            "If the user explicitly requests a different narrator gender",
            "matching Thai polite particle",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
        forbidden = (
            "target no more than 82 Unicode code points",
            "90-code-point hard fallback",
            "off-screen adult Thai woman",
            "กดตะกร้าด้านล่างได้เลยค่ะ",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.text)

    def test_ai_safe_speech_and_evidence_rules_remain(self):
        for phrase in (
            "Do not use `ๆ`",
            "เปอร์เซ็นต์",
            "restricted health, safety, durability, compatibility",
            "Do not invent claims",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_facebook_and_shopee_contracts_are_present(self):
        for phrase in (
            "exactly three to six distinct",
            "one logical line",
            "hard maximum is 150",
            "Unicode code points",
            "UTF-16 code units",
            "จำนวนอักขระ: N/150",
            "at least one complete",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_instruction_has_no_template_placeholders(self):
        for pattern in (r"\bTBD\b", r"\bTODO\b", r"\{\{[^}]+\}\}", r"<PLACEHOLDER>"):
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, self.text, re.IGNORECASE))


class ThaiQuickStartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = README_FILE.read_text(encoding="utf-8")

    def test_quick_start_names_the_instruction_file(self):
        self.assertIn("Warehouse_Affiliate_GEM_Instructions_10S.txt", self.text)

    def test_quick_start_uses_requested_gem_display_name(self):
        self.assertIn("โกดังทุบราคา 10S", self.text)
        self.assertNotIn("Warehouse Affiliate Review 10S", self.text)

    def test_quick_start_describes_direct_generation(self):
        self.assertIn("สร้างผลลัพธ์ทันที", self.text)
        self.assertIn("ภาพ 1–5 ภาพ", self.text)
        self.assertNotIn("วิธีทำงานสองรอบ", self.text)

    def test_quick_start_explains_manual_flow_handoff(self):
        for phrase in ("Gemini Omni Flash 1.1", "Frames to Video: First", "9:16", "10 วินาที", "Audio"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_quick_start_describes_new_visual_and_voice_defaults(self):
        for phrase in ("มือผู้ชาย", "เสียงผู้ชาย", "โกดังไทย", "Hook", "150–170"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)


if __name__ == "__main__":
    unittest.main()

