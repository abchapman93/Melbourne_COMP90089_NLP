import ipywidgets as widgets

class QuizHint:
    def __init__(self, description="", hints=tuple()):
        self._output = widgets.Output()
        self._num_displayed = 0


        self._description = widgets.HTML()


        self.hints = tuple()
        self.hint_values = tuple()




        self._get_hint_button = widgets.Button(description="Get hint")
        self._get_hint_button.on_click(self._show_next_hint)
        self._hide_hints_button = widgets.Button(description="Hide hints")
        self._hide_hints_button.on_click(self._hide_hints)

        self._box = None
        self._set_box()

        self.add_hints(hints)
        self.original_description = description
        self.description = self._set_description()





    def _set_description(self,):
        self.description =  self.original_description + f"</br><strong>Displaying hint {self._num_displayed}/{len(self.hints)}</strong>"
        self._description.value = self.description

    def _set_hints_button(self, disabled=True):
        self._get_hint_button.disabled = disabled

    def add_hints(self, hints):
        for hint in hints:
            self.add_hint(hint)

    def add_hint(self, hint):
        # Hide the hint until it's ready
        # hint.layout.display = "none"
        value = hint.value
        hint.value = ""
        self.hints += (hint,)
        value = f"<h4>Hint {len(self.hints)}</h4>" + value
        self.hint_values += (value,)
        self._box.children += (hint,)

    def _set_box(self, hint_button=True):
        widget_list = [self._description, self._output, ]
        if hint_button:
            widget_list.append(self._get_hint_button)
            widget_list.append(self._hide_hints_button)

        self._box = widgets.VBox(widget_list)

    def _show_next_hint(self, _):
        try:
            self.hints[self._num_displayed].value = self.hint_values[self._num_displayed]
            # self.hints[self._num_displayed].layout.display = "visible"
            self._num_displayed += 1
            self._set_description()
        except IndexError:
            print("No hints to display.")
        if self._num_displayed == len(self.hints):
            self._set_hints_button(disabled=True)

    def _hide_hints(self, _):
        for hint in self.hints:
            hint.value = ""
        self._num_displayed = 0
        self._set_hints_button(False)
        self._set_description()

    def display(self):
        """Display the Box widget in the current IPython cell."""
        from IPython.display import display as ipydisplay
        self._output.clear_output()

        ipydisplay(self._box)

    def __repr__(self):
        self.display()
        return ""