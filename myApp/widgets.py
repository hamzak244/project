# widgets.py

from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    def get_template_name(self):
        return 'widgets/multiple_file_input.html'
