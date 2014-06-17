from django import forms
from models import WFPDocument, Category
from geonode.base.models import Region
from geonode.documents.forms import DocumentForm
from geonode.layers.models import Layer
from geonode.maps.models import Map
import datetime
from django.contrib.contenttypes.models import ContentType

class WFPDocumentForm(forms.ModelForm):
    publication_date = forms.DateField(initial=datetime.date.today)
    source = forms.CharField()
    orientation = forms.ChoiceField(WFPDocument.ORIENTATION_CHOICES)
    page_format = forms.ChoiceField(WFPDocument.FORMAT_CHOICES)
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), required=False)
    regions = forms.ModelMultipleChoiceField(Region.objects.all(), required=False)
    last_version = forms.BooleanField(initial=True, required=False)
    resource = forms.ChoiceField(label='Link to')
        
    def __init__(self, *args, **kwargs):
        super(WFPDocumentForm, self).__init__(*args, **kwargs)
        # publication date
        if hasattr(self, 'instance'):
            if hasattr(self.instance, 'document'):
                self.fields['publication_date'].initial = self.instance.document.date
                
        # resource
        rbases = list(Layer.objects.all())
        rbases += list(Map.objects.all())
        rbases.sort(key=lambda x: x.title)
        rbases_choices = []
        rbases_choices.append(['no_link', '---------'])
        for obj in rbases:
            type_id = ContentType.objects.get_for_model(obj.__class__).id
            obj_id = obj.id
            form_value = "type:%s-id:%s" % (type_id, obj_id)
            display_text = '%s (%s)' % (obj.title, obj.geonode_type)
            rbases_choices.append([form_value, display_text])
        self.fields['resource'].choices = rbases_choices
        try:
            if self.instance.document.content_type:
                self.fields['resource'].initial = 'type:%s-id:%s' % (
                    self.instance.document.content_type.id, self.instance.document.object_id)
        except:
            pass
        
    class Meta:
        model = WFPDocument
        exclude = ('document',)
        
