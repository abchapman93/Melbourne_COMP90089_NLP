import ipywidgets as widgets
from random import shuffle
from .quiz import Quiz

class SelectMultipleQuiz(Quiz):
    def __init__(self, description="", answer=tuple(), options=tuple(), show_answer=False, shuffle_answer=True):
        options = list(options)
        answer = set(answer)
        for a in answer:
            if a not in options:
                options.append(a)
        super().__init__(description, answer, show_answer)

        if shuffle_answer:
            shuffle(options)
        self.options = options
        self._options = widgets.SelectMultiple(
            options=self.options
        )

        self.submitted = None
        self._submit = widgets.Button(description="Submit")
        self._submit.on_click(self._submit_answer)



        self._box = widgets.VBox(
            [
                self._description,
                self._options,
                self._submit,
                self._response,
                self._output

            ]
        )

    def _submit_answer(self, change):
        self.submitted = self._options.value
        self._validate_answer()

    def _validate_answer(self):
        # If there's already a response, remove it
        submitted = set(self.submitted)
        actual = set(self.answer)

        # Check if their are any differences
        if submitted == actual:
            self.response = "That is correct!"
        else:
            self.response = f"That is incorrect. " \
                            f"You have selected {len(submitted.intersection(actual))}/{len(actual)} " \
                            f"correct answers."
            if self.show_answer:
                self.response += f" Expected '{self.answer}'. Got '{self.submitted}'"

        self._response.value = self.response

