import unittest

from main import greetings, is_palindrome


class ExampleTest(unittest.TestCase):
    @greetings
    def name_surname(self):
        return "joe doe"

    def test_result(self):
        self.assertEqual(self.name_surname(), "Hello Joe Doe")

    @is_palindrome
    def show_sentence(self):
        return "annA"

    def test_result(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")


if __name__ == "__main__":
    unittest.main()