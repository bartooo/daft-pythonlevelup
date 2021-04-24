import unittest

from main import (
    greetings,
    is_palindrome,
    format_output,
    add_class_method,
    add_instance_method,
)


class A:
    pass


class ExampleTest(unittest.TestCase):
    @greetings
    def name_surname(self):
        return "joe doe"

    @is_palindrome
    def show_sentence(self):
        return "annA"

    @format_output("first_name__last_name", "city")
    def first_func(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "city": "Warszawa",
        }

    @format_output("first_name", "age")
    def second_func(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "city": "Warszawa",
        }

    @add_class_method(A)
    def foo():
        return "Hello!"

    @add_instance_method(A)
    def bar():
        return "Hello again!"

    def test_result(self):
        self.assertEqual(self.name_surname(), "Hello Joe Doe")
        self.assertEqual(self.show_sentence(), "annA - is palindrome")
        self.assertEqual(
            self.first_func(),
            {"first_name__last_name": "Jan Kowalski", "city": "Warszawa"},
        )
        self.assertRaises(ValueError, self.second_func)
        self.assertEqual(A.foo(), "Hello!")
        self.assertEqual(A().bar(), "Hello again!")


if __name__ == "__main__":
    unittest.main()