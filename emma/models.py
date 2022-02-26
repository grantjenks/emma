from django.db import models


class Screenshot(models.Model):
    num = models.IntegerField()
    time = models.DateTimeField()
    image = models.ImageField(upload_to='screenshots/%Y/%m/%d/%H/%M/')
