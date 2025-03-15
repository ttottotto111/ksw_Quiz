from django.db import models

# Create your models here.
class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    questions_count = models.IntegerField(default = 10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, related_name="quiz_id",on_delete=models.CASCADE)
    title = models.TextField()
    answer = models.JSONField()
    correct_answer = models.CharField(max_length=100)