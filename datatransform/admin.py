from django.contrib import admin
from datatransform.models import PublishData, models
from django_json_widget.widgets import JSONEditorWidget
# Register your models here.

class SingletonPageAdmin(admin.ModelAdmin):
    formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget(attrs={'style':'height:500px'})}}
admin.site.register(PublishData, SingletonPageAdmin)
