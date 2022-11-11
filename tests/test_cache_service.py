import unittest
from services import cache_service


class CacheServiceTest(unittest.TestCase):

	def test_set_cache(self):
		service_cache = cache_service.BasicCache()
		expected_dict = {"test": "value"}

		service_cache["test"] = "value"
		self.assertDictEqual(service_cache.cache, expected_dict)

	def test_get_cache(self):
		service_cache = cache_service.BasicCache()
		expected_value= "value"

		service_cache["test"] = "value"

		self.assertEqual(service_cache["test"], expected_value)