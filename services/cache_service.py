from functools import cache


SERVICE_NAME = "cache"


class BasicCache():
	cache = {}

	def __init__(self, data_location_key=None):
		if data_location_key:
			self.cache[data_location_key] = {}

	def __getitem__(self, key):
		if key in self.cache:
			return self.cache[key]

	def __setitem__(self, key, value):
		self.cache[key] = value