import re
import unittest
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "tests" / "fixtures" / "behavior-cases.md"

REQUIRED_CASES = {
    "single-clear-image",
    "single-mixed-marketplace-image",
    "multiple-products",
    "conflicting-required-promotion",
    "conditional-promotion",
    "expired-promotion",
    "explicit-gender-override",
    "unsupported-optional-claim",
    "latest-user-direction",
    "male-hands-default",
    "adult-male-explicit",
    "hook-only-added-text",
    "verified-price-hook",
    "product-identity-lock",
    "male-voice-150-170",
    "shopee-150",
    "shopee-151",
    "emoji-count",
}


def parse_cases(text):
    matches = list(re.finditer(r"^## CASE: ([a-z0-9-]+)\s*$", text, re.MULTILINE))
    cases = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        cases[match.group(1)] = text[match.end():end]
    return cases


def conservative_count(payload):
    normalized = unicodedata.normalize("NFC", payload)
    return max(len(normalized), len(normalized.encode("utf-16-le")) // 2)


def extract_logical_payload(rendered):
    if rendered.endswith("\r\n"):
        payload = rendered[:-2]
    elif rendered.endswith("\n"):
        payload = rendered[:-1]
    else:
        payload = rendered
    if "\r" in payload or "\n" in payload:
        raise ValueError("payload contains a line break")
    if payload != payload.strip():
        raise ValueError("payload contains outer whitespace")
    return unicodedata.normalize("NFC", payload)


class ScenarioCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CATALOG.read_text(encoding="utf-8")
        cls.cases = parse_cases(cls.text)

    def test_all_required_cases_exist_without_stale_confirmation_cases(self):
        self.assertEqual(REQUIRED_CASES, set(self.cases))
        self.assertNotIn("AWAITING_CONFIRMATION", self.text)
        self.assertNotIn("bare `ยืนยัน`", self.text)

    def test_every_case_has_required_sections(self):
        for case_id, body in self.cases.items():
            with self.subTest(case_id=case_id):
                self.assertRegex(body, r"(?m)^### Input\s*$")
                self.assertRegex(body, r"(?m)^### Expected state\s*$")
                self.assertRegex(body, r"(?m)^### Expected behavior\s*$")

    def test_every_case_declares_a_current_state(self):
        for case_id, body in self.cases.items():
            match = re.search(r"(?ms)^### Expected state\s*\n+([^\n]+)", body)
            self.assertIsNotNone(match, case_id)
            with self.subTest(case_id=case_id):
                self.assertIn(match.group(1).strip(), ("NEEDS_INPUT", "FINAL", "FINAL after shortening"))

    def test_only_genuine_blockers_need_input(self):
        expected = {
            "single-clear-image": "FINAL",
            "single-mixed-marketplace-image": "FINAL",
            "multiple-products": "NEEDS_INPUT",
            "conflicting-required-promotion": "NEEDS_INPUT",
            "conditional-promotion": "FINAL",
            "expired-promotion": "FINAL",
            "explicit-gender-override": "FINAL",
            "unsupported-optional-claim": "FINAL",
            "latest-user-direction": "FINAL",
            "male-hands-default": "FINAL",
            "adult-male-explicit": "FINAL",
            "hook-only-added-text": "FINAL",
            "verified-price-hook": "FINAL",
            "product-identity-lock": "FINAL",
            "male-voice-150-170": "FINAL",
        }
        for case_id, want in expected.items():
            match = re.search(r"(?ms)^### Expected state\s*\n+([^\n]+)", self.cases[case_id])
            with self.subTest(case_id=case_id):
                self.assertEqual(want, match.group(1).strip())

    def test_core_new_behaviors_are_explicit(self):
        requirements = {
            "single-clear-image": ("without confirmation", "four final blocks"),
            "latest-user-direction": ("apply it immediately", "do not ask for confirmation"),
            "male-hands-default": ("one left hand and one right hand", "same adult man"),
            "adult-male-explicit": ("only because the user explicitly requested",),
            "hook-only-added-text": ("exactly one Thai Hook", "no price signage"),
            "verified-price-hook": (
                "19 บาท ได้ 10 ใบ ปกติ 69 บาท",
                "exactly as the single Hook",
                "no other generated price signage",
            ),
            "product-identity-lock": ("same product throughout", "no spin or rotation"),
            "male-voice-150-170": ("150–170", "กดตะกร้าด้านล่างได้เลยครับ"),
            "explicit-gender-override": ("hands, visible demonstrator, voice, and CTA", "matching polite particle"),
        }
        for case_id, phrases in requirements.items():
            for phrase in phrases:
                with self.subTest(case_id=case_id, phrase=phrase):
                    self.assertIn(phrase, self.cases[case_id])

    def test_boundary_cases_pin_literal_payload_and_count(self):
        expected = {"shopee-150": 150, "shopee-151": 151, "emoji-count": 14}
        for case_id, want in expected.items():
            body = self.cases[case_id]
            payload = re.search(r"(?m)^Literal payload: `(.*)`$", body).group(1)
            declared = int(re.search(r"(?m)^Expected conservative count: (\d+)$", body).group(1))
            with self.subTest(case_id=case_id):
                self.assertEqual(want, declared)
                self.assertEqual(want, conservative_count(payload))

    def test_renderer_structural_newline_rule(self):
        payload = "สินค้า #บ้าน"
        for rendered in (payload, payload + "\n", payload + "\r\n"):
            with self.subTest(rendered=repr(rendered)):
                self.assertEqual(payload, extract_logical_payload(rendered))
        for rendered in (payload + " ", " " + payload, payload + "\n\n", payload + "\r\n\r\n"):
            with self.subTest(rendered=repr(rendered)):
                with self.assertRaises(ValueError):
                    extract_logical_payload(rendered)


if __name__ == "__main__":
    unittest.main()
