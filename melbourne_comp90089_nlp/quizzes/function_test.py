HINT_MSG = "Incorrect value. Expected {expected}, got {actual}"

class FunctionTest:
    def __init__(self, args=None, expected=None, validation_func=None, give_hint=False, hint_msg=""):
        self.args = args
        self.expected = expected
        self.validation_func = validation_func
        self.give_hint = give_hint
        self.hint_msg = hint_msg


    def test(self, func):
        try:
            if self.validation_func is not None:
                self.test_validation_func(func)
            else:
                actual = func(*self.args)
                assert actual == self.expected
                print("Correct!")
        except AssertionError:
            msg = "Incorrect."
            if self.give_hint is True:
                msg += self.hint_msg.format(**self.__attr__)
            print(msg)
        except Exception as e:
            print("Error raised during test.")
            raise e

    def test_validation_func(self, submitted_func):
        self.validation_func(submitted_func)

