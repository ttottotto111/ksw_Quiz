from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

from .models import BoardSetting

class QuizPagination(PageNumberPagination):
    def get_page_size(self, request):
        try:
            quiz_page_size = BoardSetting.objects.first().quiz_paging
            cache.set("pagination_size", quiz_page_size, timeout = 3600)
            return quiz_page_size
        except:
            cache.set("pagination_size", 10)
            return 10

class QuestionPagination(PageNumberPagination):
    def get_page_size(self, request):
        try:
            question_page_size = BoardSetting.objects.first().question_paging
            cache.set("pagination_size", question_page_size, timeout = 3600)
            return question_page_size
        except:
            cache.set("pagination_size", 10)
            return 10