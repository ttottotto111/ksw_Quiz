from django.db import models

# Create your models here.
class BoardSetting(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_paging = models.IntegerField(default=10)
    question_paging = models.IntegerField(default = 10)
    question_random = models.BooleanField(default=False)
    choice_random = models.BooleanField(default = False)