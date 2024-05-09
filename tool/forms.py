from django import forms


class zipForm(forms.Form):
    zip_file = forms.FileField()