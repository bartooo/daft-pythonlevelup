def greetings(foo):
    def to_capital(self):
        return "Hello " + " ".join(i.capitalize() for i in foo(self).split(" "))

    return to_capital


def is_palindrome(sentence):
    def check_if_palindrome(self):
        filtered_s = "".join(filter(str.isalnum, sentence(self)))
        if filtered_s[::-1].lower() == filtered_s.lower():
            return sentence(self) + " - is palindrome"
        else:
            return sentence(self) + " - is not palindrome"

    return check_if_palindrome


def format_output():
    pass