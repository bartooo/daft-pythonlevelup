import unittest

from main import greetings


class ExampleTest(unittest.TestCase):
    @greetings
    def name_surname(self):
        return "joe doe"

    def test_result(self):
        self.assertEqual(self.name_surname(), "Hello Joe Doe")


if __name__ == "__main__":
    unittest.main()