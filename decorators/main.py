from functools import wraps


def greetings(foo):
    @wraps(foo)
    def to_capital(*args, **kwargs):
        return "Hello " + " ".join(
            i.capitalize() for i in foo(*args, **kwargs).split(" ")
        )

    return to_capital


def is_palindrome(sentence):
    @wraps(sentence)
    def check_if_palindrome(*args, **kwargs):
        filtered_s = "".join(filter(str.isalnum, sentence(*args, **kwargs)))
        if filtered_s[::-1].lower() == filtered_s.lower():
            return sentence(*args, **kwargs) + " - is palindrome"
        else:
            return sentence(*args, **kwargs) + " - is not palindrome"

    return check_if_palindrome


def format_output(*dec_args):
    def inner(foo):
        def find_args(*args, **kwargs):
            res_dict = dict()
            for arg in dec_args:
                a_splt = arg.split("__")
                res = []
                for a in a_splt:
                    if a not in foo(*args, **kwargs).keys():
                        raise ValueError
                    res.append(foo(*args, **kwargs)[a])

                res_dict[arg] = " ".join(res)

            return res_dict

        return find_args

    return inner


def add_class_method(cls):
    def inner(methd):
        def wrapper(*args, **kwargs):
            return methd(*args, **kwargs)

        setattr(cls, methd.__name__, wrapper)

        return wrapper

    return inner


def add_instance_method(cls):
    def inner(methd):
        def wrapper(self, *args, **kwargs):
            return methd(*args, **kwargs)

        setattr(cls, methd.__name__, wrapper)

        return methd

    return inner
