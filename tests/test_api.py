import unittest

from arab_prompts.catalog import categories, get_prompt, prompts, search

class PackageTests(unittest.TestCase):
    def test_package_loads_bundled_catalog(self):
        self.assertEqual(len(prompts()), 1650)
        self.assertEqual(len(categories()), 17)

    def test_lookup_and_lexical_search(self):
        self.assertEqual(get_prompt(1)["id"], 1)
        results = search("إعلان فيسبوك")
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], 1)

if __name__ == "__main__":
    unittest.main()
