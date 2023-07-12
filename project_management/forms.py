from django import forms
from .models import TaskSuppFile


class SuppFileUploadForm(forms.ModelForm):
    class Meta:
        model = TaskSuppFile
        fields = ['supplementary_file']
