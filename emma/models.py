from django.db import models


class Screenshot(models.Model):
    display = models.IntegerField()
    time = models.DateTimeField()
    image = models.ImageField(upload_to='screenshots/%Y/%m/%d/%H/%M/')
