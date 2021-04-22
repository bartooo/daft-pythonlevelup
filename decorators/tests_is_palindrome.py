import unittest

from main import is_palindrome


class ExampleTest(unittest.TestCase):
    @is_palindrome
    def show_sentence(self):
        return "annA"

    def test_result(self):
        self.assertEqual(self.show_sentence(), "annA - is palindrome")


if __name__ == "__main__":
    unittest.main()