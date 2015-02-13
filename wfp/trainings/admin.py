from django.contrib import admin
from wfp.trainings.models import Training

class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_layers',)
    search_fields = ('title', 'abstract',)

admin.site.register(Training, TrainingAdmin)
