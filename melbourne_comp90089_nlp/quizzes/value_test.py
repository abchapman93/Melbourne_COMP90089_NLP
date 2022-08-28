class ValueTest():

    def __init__(self, expected=3, show_answer=False, validation_func=None):
        self.validation_func = validation_func
        self.expected = expected
        self.show_answer = show_answer

    def test(self, actual):
        if self.validation_func is not None:
            return self.validation_func(actual)
        if self.expected != actual:
            msg = "That is incorrect."
            if self.show_answer:
                msg += f" Expected {self.expected}, got {actual}"
            print(msg)
        else:
            print("That is correct!")

    def test_validation_func(self, actual):
        self.validation_func(actual)