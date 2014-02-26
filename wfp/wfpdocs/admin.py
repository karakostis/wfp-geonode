from django.contrib import admin
from wfp.wfpdocs.models import WFPDocument, Category

class WFPDocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'get_date', 'get_date_type', 'get_regions', 
        'source', 'get_categories', 'orientation', 'format', )
    list_display_links = ('document',)
    list_filter  = ('orientation', 'format', 'categories' )
    search_fields = ('document__title',)
    #date_hierarchy = 'date'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
        
admin.site.register(WFPDocument, WFPDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
