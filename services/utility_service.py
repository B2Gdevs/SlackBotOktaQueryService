from logging import debug
from typing import Union
import yaml
import re
from loguru import logger
from commonregex import CommonRegex


SERVICE_NAME = "utility"


def load_yaml_data(path: str) -> dict:
	"""Conventiently parse given yaml file and return a dict.

	Parameters
	----------
	path : str
		File path to the yaml file.

	Returns
	-------
	dict
		A dict with the loaded yaml file in memory.
	"""
	with open(path, "r") as file:
		return yaml.safe_load(file)


def parse_chat_protocol(user_chat_text: str) -> Union[str, list[str]]:
	"""Parse text in wallee chat bot using wallees protocol.

	Protocol format:
	{Verb} {identifier}? {attribute1}? {attribute2}? ...

	Parameters
	----------
	user_chat_text : str
		The chat protocol string.

	Returns
	-------
	str :
		The verb associated with the message.
	list[str] :
		The rest of the query.
	"""
	split_text = user_chat_text.split()
	# TODO: Make this support the {verb} {service} {param1} {param2} protocol
	return split_text[0], split_text[1:] if len(split_text) > 1 else []


def extract_assignments(query_params: list[str]) -> dict:
	"""Extract any assignment text found in each param token.

	Parameters
	----------
	query_params : list[str]
			A list of tokens found in the chat query.

	Returns
	-------
	dict
			A dictionary with the keys as the fields to be assigned and the values as
			the values to be assigned to the fields.
	"""
	assignment_dict = {}
	field = None
	for assignment in query_params:
		match = re.search(r"([^=]*)=", assignment)
		if match:
			field_split = assignment.split("=")
			field = field_split[0]
			assignment_dict[field] = field_split[1]
			continue

		if field is None:
			continue

		# Since spaces can occur, if it is not detected to a be a field
		# then it is the value
		assignment_dict[field] += f" {assignment}"
	return assignment_dict


def extract_email(query_string: str) -> str or None:
	"""Extract an email in any given format.

	Parameters
	----------
	query_string : str
			A string that has an email.

	Returns
	-------
	str or None
			The first matching string or nothing.
	"""
	regex_obj = CommonRegex(query_string)
	if len(regex_obj.emails) > 0:
		return regex_obj.emails[0]
