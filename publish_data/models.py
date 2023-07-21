from django.db import models

# Create your models here.

class CloudPublishData(models.Model):
    msg_type    = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=255)
    device_id   = models.CharField(max_length=255)
    data        = models.JSONField()
    created_on  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self) -> str:
        return self.msg_type
    
    
