import ipywidgets as widgets

class Quiz:
    def __init__(self, description="", answer=None, show_answer=False):
        self._output = widgets.Output()
        self.description = description
        self._description = widgets.HTML(value=self.description)
        self.answer = answer

        self.submitted = None
        self._submit = widgets.Button(description="Submit")
        self._submit.on_click(self._submit_answer)

        self.response = ""
        self._response = self._response = widgets.HTML(
            value=self.response
        )

        self._box = None
        self._set_box()



        self.show_answer = show_answer

    def _set_box(self):
        self._box = widgets.VBox(
            [
                self._description,
                self._output,
                self._response

            ]
        )

    def display(self):
        """Display the Box widget in the current IPython cell."""
        from IPython.display import display as ipydisplay
        self._output.clear_output()

        ipydisplay(self._box)

    def _submit_answer(self, change):
        self.submitted = self._options.value
        self._validate_answer()

    def _validate_answer(self):
        # If there's already a response, remove it
        if self.submitted == self.answer:
            self.response = "That is correct!"
        else:
            self.response = "That is incorrect."
            if self.show_answer:
                self.response += f" Expected '{self.answer}'. Got '{self.submitted}'"

        self._response.value = self.response

    def __repr__(self):
        self.display()
        return ""