import os
import datetime
import json

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import HiddenInput, TextInput
from django.conf import settings

from geonode.base.models import Region
from geonode.documents.forms import DocumentForm
from geonode.layers.models import Layer
from geonode.maps.models import Map

from models import WFPDocument, Category

class WFPDocumentForm(forms.ModelForm):
    """
    For to upload Static Maps.
    """
    permissions = forms.CharField(
        widget=HiddenInput(
            attrs={
                'name': 'permissions',
                'id': 'permissions'}),
        required=True)
    publication_date = forms.DateTimeField(widget=forms.SplitDateTimeWidget)

    def __init__(self, *args, **kwargs):
        super(WFPDocumentForm, self).__init__(*args, **kwargs)
        # publication date
        if hasattr(self.instance, 'document'):
            self.fields['publication_date'].initial = self.instance.document.date
        else:
            self.fields['publication_date'].widget.widgets[0].attrs = {'class':'datepicker', 'data-date-format': 'yyyy-mm-dd', 'value': str(datetime.date.today())}
            self.fields['publication_date'].widget.widgets[1].attrs = {"class":"time",
        'value': datetime.datetime.now().strftime('%H:%M:%S')}
        
    class Meta:
        model = WFPDocument
        fields = ('title', 'doc_file', 'source', 'orientation', 'page_format', 'categories', 'regions',
            'last_version', 'layers', 'keywords',
        )
        
    def clean_doc_file(self):
        """
        Ensures the doc_file is valid.
        """
        doc_file = self.cleaned_data.get('doc_file')

        if doc_file and not os.path.splitext(
                doc_file.name)[1].lower()[
                1:] in ('gif', 'jpg', 'jpeg', 'pdf', 'png'):
            raise forms.ValidationError(_("This file type is not allowed"))

        return doc_file
    
    def clean_permissions(self):
        """
        Ensures the JSON field is JSON.
        """
        permissions = self.cleaned_data['permissions']

        try:
            return json.loads(permissions)
        except ValueError:
            raise forms.ValidationError(_("Permissions must be valid JSON."))
