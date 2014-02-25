from django.contrib import admin
from wfp.wfpdocs.models import WFPDocument, Category

class WFPDocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'get_date', 'get_date_type', 'get_regions', 
        'source', 'get_categories', 'orientation', 'format', )
    list_display_links = ('document',)
    list_filter  = ('orientation', 'format', 'categories' )
    search_fields = ('document__title',)
    #date_hierarchy = 'date'
    
    def get_date(self, obj):
        return obj.document.date.isoformat()
    get_date.short_description = 'Date'
    
    def get_regions(self, obj):
        regions = ''
        for region in obj.document.regions.all():
            regions += '%s ' % region.name
        return regions
    get_regions.short_description = 'Regions'
    
    def get_categories(self, obj):
        categories = ''
        for category in obj.categories.all():
            categories += '%s ' % category.name
        return categories
    get_categories.short_description = 'Categories'
    
    def get_date_type(self, obj):
        return obj.document.date_type
    get_date_type.short_description = 'Date Type'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
        
admin.site.register(WFPDocument, WFPDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
