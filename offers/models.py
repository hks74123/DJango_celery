from msilib.schema import Class
from django.db import models
from .tasks import send_mail
# Create your models here.

class offers(models.Model):
    title = models.CharField(max_length=20)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def save(self, *args, **kwargs):
        send_mail.delay()
        super(offers, self).save(*args, **kwargs)