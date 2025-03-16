from django.db import models
from django.contrib.auth.models import User
from quiz_manager.models import Quiz

# Create your models here.
class History(models.Model):
    user_id = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, related_name="quiz", on_delete=models.CASCADE)
    question_count = models.IntegerField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)