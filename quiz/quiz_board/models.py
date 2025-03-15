from django.db import models

# Create your models here.
class BoardSetting(models.Model):
    setting = models.CharField(primary_key=True, max_length=100)
    value = models.IntegerField()