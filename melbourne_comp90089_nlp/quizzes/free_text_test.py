from ipywidgets import widgets
from .quiz import Quiz

class FreeTextTest(Quiz):
    def __init__(self, description="", answer="", show_answer=False, preprocessor=None,
                 validation_func=None):
        self.preprocessor = preprocessor
        self.validation_func = validation_func

        super().__init__(description, answer, show_answer)
        if type(answer) in (str, int, float):
            answer = [str(answer)]
        self.answer = [str(a).replace("\'", "\"") for a in answer]
        if self.preprocessor is not None:
            self.answer = [self.preprocessor(a) for a in answer]
        self.entered = None

        self._entry = widgets.Textarea(
            value=None,
            placeholder='Type something',
        )

        self._box = widgets.VBox(
            [
                self._description,
                self._entry,
                self._submit,
                self._response,
                self._output

            ]
        )

    def _submit_answer(self, change):
        self.entered = self._entry.value.strip().replace("\'", "\"")
        if self.preprocessor is not None:
            self.entered = self.preprocessor(self.entered)
        self._validate_answer()

    def _validate_answer(self):
        if self.validation_func is not None:
            result = any([self.validation_func(x) for x in self.entered])
        else:
            result = self.entered in self.answer
        if result:
            self.response = "That is correct!"
        else:
            self.response = "That is incorrect."
        self._response.value = self.response

    def display(self):
        """Display the Box widget in the current IPython cell."""
        from IPython.display import display as ipydisplay
        self._output.clear_output()

        ipydisplay(self._box)

    def __repr__(self):
        self.display()
        return ""