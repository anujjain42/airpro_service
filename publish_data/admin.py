from django.contrib import admin

from publish_data.models import CloudPublishData
# Register your models here.

@admin.register(CloudPublishData)
class CloudPublishDataAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'mac_address', 'device_id',  'created_on', ]