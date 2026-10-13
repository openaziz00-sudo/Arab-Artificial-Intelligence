import unittest

from fastapi.testclient import TestClient

from api.main import app
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

class EndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_and_categories(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["prompts"], 1650)
        categories_response = self.client.get("/categories")
        self.assertEqual(categories_response.status_code, 200)
        self.assertEqual(len(categories_response.json()["categories"]), 17)

    def test_prompt_listing_and_detail(self):
        listing = self.client.get("/prompts", params={"category": "code", "limit": 2})
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(len(listing.json()["items"]), 2)
        detail = self.client.get("/prompts/1")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json()["id"], 1)
        self.assertEqual(self.client.get("/prompts/99999").status_code, 404)

    def test_lexical_search_endpoint(self):
        response = self.client.get("/search", params={"q": "إعلان فيسبوك", "semantic": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["mode"], "lexical")
        self.assertTrue(response.json()["items"])

    def test_search_validation(self):
        self.assertEqual(self.client.get("/search").status_code, 422)
        self.assertEqual(self.client.get("/search", params={"q": "x", "category": "missing", "semantic": "false"}).status_code, 404)

if __name__ == "__main__":
    unittest.main()
