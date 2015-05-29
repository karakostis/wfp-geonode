from django.contrib import admin
from wfp.wfpdocs.models import WFPDocument, Category
from account.models import EmailAddress


class WFPDocumentAdmin(admin.ModelAdmin):
    """
    Admin for a static map.
    """
    list_display = ('title', 'date', 'date_updated', 'get_layers',
        'get_regions', 'source', 'get_categories', 'orientation', 'page_format',
        'extension', )
    list_display_links = ('title',)
    list_filter  = ('orientation', 'page_format', 'categories', 'extension',
        'regions',)
    search_fields = ('title',)
    date_hierarchy = 'date'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(WFPDocument, WFPDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
