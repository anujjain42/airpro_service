from django.db import models

# Create your models here.

class APDevice(models.Model):
    serial_number   = models.CharField(max_length=100, unique=True)
    alias           = models.CharField(max_length=100)
    client_topic    = models.CharField(max_length=100, blank=True, null=True)
    server_topic    = models.CharField(max_length=100, blank=True, null=True)
    port            = models.IntegerField(default=1883)
    broker_ip       = models.GenericIPAddressField(blank=True, null=True)
    mac_address     = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.serial_number) 