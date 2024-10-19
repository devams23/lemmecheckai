from django import forms
from .models import PDFUpload

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ['pdf_file']
