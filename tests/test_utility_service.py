import unittest
from services import utility_service


class UtilityServiceTest(unittest.TestCase):

    def test_email_extraction(self):
        email1 = "query adam.ian@example.com title"
        email2 = "query <mailto:example@test.ai|example@test.ai> title"
        email3 = "query ian@example.com title"

        extracted_email = utility_service.extract_email(email1)
        self.assertEqual(extracted_email, "adam.ian@example.com")

        extracted_email = utility_service.extract_email(email2)
        self.assertEqual(extracted_email, "example@test.ai")

        extracted_email = utility_service.extract_email(email3)
        self.assertEqual(extracted_email, "ian@example.com")

    def test_parse_chat_protocol(self):
        protocol1 = "create someemail@example.com title=name desc=description"
        expected_verb = "create"
        expected_params = ["someemail@example.com", "title=name", "desc=description"]
        verb, params = utility_service.parse_chat_protocol(protocol1)
        self.assertEqual(expected_verb, verb)
        self.assertEqual(expected_params, params)

    def test_extract_assignments(self):
        protocol1 = "create someemail@example.com title=name desc=some description"
        expected_assignments = {"title": "name",
                                "desc": "some description"}
        _, params = utility_service.parse_chat_protocol(protocol1)
        assignments = utility_service.extract_assignments(params)
        self.assertEqual(expected_assignments, assignments)


if __name__ == '__main__':
    unittest.main()