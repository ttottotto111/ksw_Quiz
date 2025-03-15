from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_item(sender, **kwargs):
    from .models import BoardSetting
    if not BoardSetting.objects.exists():
        BoardSetting.objects.create()

class QuizBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz_board'
    
    def ready(self):
        post_migrate.connect(create_default_item, sender=self)