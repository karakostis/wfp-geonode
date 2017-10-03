import autocomplete_light
from models import WFPDocument

class WFPDocumentWfpDocsAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    choice_template = 'autocomplete_response.html'

autocomplete_light.register(
    WFPDocument,
    WFPDocumentWfpDocsAutocomplete,
    search_fields=['title'],
    order_by=['title'],
    limit_choices=30,
    autocomplete_js_attributes={
        'placeholder': 'Staticmap name..',
    },
)
