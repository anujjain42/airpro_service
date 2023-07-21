from django.db import models

# Create your models here.

class PublishData(models.Model):
    msg_type    = models.PositiveIntegerField()
    data        = models.JSONField()

    def __str__(self) -> str:
        return str(self.msg_type)