from django import forms
from models import WFPDocument, Category

class DocumentForm(forms.Form):
    source = forms.CharField()
    orientation = forms.ChoiceField(WFPDocument.ORIENTATION_CHOICES)
    format = forms.ChoiceField(WFPDocument.FORMAT_CHOICES)
    categories = forms.ModelMultipleChoiceField(Category.objects.all())
