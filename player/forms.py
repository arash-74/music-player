from django import forms


class UploadForm(forms.Form):
    uploader = forms.FileField()
