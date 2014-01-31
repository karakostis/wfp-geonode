from django.contrib import admin
from account.models import EmailAddress

class EmailAddressAdmin(admin.ModelAdmin):
    model = EmailAddress
    list_display = ('user', 'email', 'verified')
    list_filter = ('verified',)
    #search_fields = ('name', 'workspace',)
    
admin.site.register(EmailAddress, EmailAddressAdmin)
