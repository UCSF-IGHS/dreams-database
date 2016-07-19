from django import forms


class EnrollmentDocumentUpload(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=True,
    )