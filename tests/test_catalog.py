"""Integrity checks for the static prompt catalog."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "prompts.json"
INDEX_PATH = ROOT / "index.html"
README_PATH = ROOT / "README.md"
EXPECTED_PROMPTS = 1650
EXPECTED_CATEGORIES = 17
REQUIRED_FIELDS = {
    "id", "category", "title", "prompt", "summary", "model",
    "settings", "example", "tip",
}


class CatalogIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.records = cls.data["prompts"]
        cls.categories = cls.data["categories"]

    def test_catalog_has_expected_totals(self) -> None:
        self.assertEqual(len(self.records), EXPECTED_PROMPTS)
        self.assertEqual(len(self.categories), EXPECTED_CATEGORIES)

    def test_catalog_top_level_shape(self) -> None:
        self.assertIsInstance(self.data, dict)
        self.assertIsInstance(self.records, list)
        self.assertIsInstance(self.categories, dict)
        self.assertTrue(all(isinstance(key, str) and isinstance(label, str) and label.strip()
                            for key, label in self.categories.items()))

    def test_every_record_has_required_nonempty_fields(self) -> None:
        for index, record in enumerate(self.records, start=1):
            with self.subTest(record=index):
                self.assertIsInstance(record, dict)
                self.assertTrue(REQUIRED_FIELDS.issubset(record))
                for field in REQUIRED_FIELDS - {"id"}:
                    self.assertIsInstance(record[field], str)
                    self.assertTrue(record[field].strip(), f"record {index}: empty {field}")
                self.assertIsInstance(record["id"], int)
                self.assertNotIsInstance(record["id"], bool)

    def test_ids_are_unique_and_sequential(self) -> None:
        self.assertEqual([record["id"] for record in self.records],
                         list(range(1, EXPECTED_PROMPTS + 1)))

    def test_titles_and_prompts_are_unique(self) -> None:
        titles = [record["title"].strip().casefold() for record in self.records]
        prompts = [record["prompt"].strip() for record in self.records]
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(prompts), len(set(prompts)))

    def test_every_record_references_a_known_category(self) -> None:
        for record in self.records:
            self.assertIn(record["category"], self.categories,
                          f"unknown category on id {record['id']}")

    def test_interface_and_readme_match_catalog_totals(self) -> None:
        html = INDEX_PATH.read_text(encoding="utf-8")
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn(f"<strong>{EXPECTED_PROMPTS}</strong>", html)
        self.assertIn(f"catalog.length!=={EXPECTED_PROMPTS}", html)
        self.assertIn("تضم ١٬٦٥٠ برومبتًا في ١٧ فئة", html)
        self.assertIn("١٧ فئة", readme)
        self.assertIn("١٬٦٥٠", readme)


if __name__ == "__main__":
    unittest.main()
