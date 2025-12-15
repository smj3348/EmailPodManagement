from django import forms

class VpsCsvImportForm(forms.Form):
    csv_file = forms.FileField(help_text="Upload a CSV exported from your VPS template.")
