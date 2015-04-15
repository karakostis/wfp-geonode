from django.contrib import admin

from models import Service, ServiceLayer


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'method')
    list_display_links = ('id', 'name', )
    list_filter = ('type', 'method')


class ServiceLayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'layer', 'typename')
    list_display_links = ('id', )
    list_filter = ('typename', 'service')

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceLayer, ServiceLayerAdmin)
