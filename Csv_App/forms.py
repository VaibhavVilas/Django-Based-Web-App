from django import forms

# defining a form to upload files


class UploadForm(forms.Form):
    file = forms.FileField()
