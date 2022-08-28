import ipywidgets as widgets
from random import shuffle
from .quiz import Quiz

class MultipleChoiceQuiz(Quiz):
    def __init__(self, description="", answer="True", options=("True", "False"), show_answer=False, shuffle_answer=True):
        options = list(options)
        if answer not in options:
            options.append(answer)
        super().__init__(description, answer, show_answer)

        if shuffle_answer:
            shuffle(options)
        self.options = options
        self._options = widgets.RadioButtons(
            options=self.options,
            layout=widgets.Layout(width='auto')
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
