from django.contrib import admin
from wfp.wfpdocs.models import WFPDocument, Category
from account.models import EmailAddress

class WFPDocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'get_date', 'get_date_type', 'date_updated',
        'get_regions', 'source', 'get_categories', 'orientation', 'page_format', )
    list_display_links = ('document',)
    list_filter  = ('orientation', 'page_format', 'categories' )
    search_fields = ('document__title',)
    #date_hierarchy = 'date'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
        
admin.site.register(WFPDocument, WFPDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
