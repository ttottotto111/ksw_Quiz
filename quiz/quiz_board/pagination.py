from rest_framework.pagination import PageNumberPagination
from .utils import get_board_setting

class QuizPagination(PageNumberPagination):
    def get_page_size(self, request):
        setting = get_board_setting()
        return setting.quiz_paging

class QuestionPagination(PageNumberPagination):
    def get_page_size(self, request):
        setting = get_board_setting()
        return setting.question_paging