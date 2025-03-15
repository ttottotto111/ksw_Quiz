from django.shortcuts import render
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
import random
import itertools
import copy

from .pagination import QuizPagination, QuestionPagination

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser

from .serializers import SettingSerializers, QuizSerializers, QuestionsSerializers

from .models import BoardSetting
from quiz_manager.models import Quiz

# Create your views here.
class Setting(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    
    queryset = BoardSetting.objects.all()
    serializer_class = SettingSerializers
    
    http_method_names = ['get', 'put', 'patch']
    
    def perform_update(self, serializer):
        cache.delete("pagination_size")
        
        return super().perform_update(serializer)

class QuizBoard(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all().order_by("-created_at")
    serializer_class = QuizSerializers
    pagination_class = QuizPagination
    
    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        
        # 랜덤 확인
        setting = BoardSetting.objects.first()
        question_random = setting.question_random
        choice_random = setting.choice_random
        # 설정된 질문 개수 확인
        question_count = quiz.questions_count
        # 전체 질문
        questions = list(quiz.quiz_id.all())
        
        # 질문개수가 많을경우
        if len(questions) >= question_count:
            if question_random:
                question_list = random.sample(questions, question_count)
            else:
                question_list = questions[:question_count]
        # 질문개수가 부족할 경우
        else:
            #부족한 개수
            shortage = question_count - len(questions)
            if question_random:
                random_question = random.choices(questions, k=shortage)
                question_list = questions + random_question
                random.shuffle(question_list)
            else:
                # 랜덤이 아닐경우 순서대로 반복
                question_list = list(itertools.islice(itertools.cycle(questions), question_count))
        
        # 선택지 랜덤 설정
        if choice_random:
            for idx, question in enumerate(question_list):
                question_copy = copy.deepcopy(question)
                answer = question_copy.answer[:]
                random.shuffle(answer)
                question_copy.answer = answer
                question_list[idx] = question_copy
            
        paginator = QuestionPagination()
        question_paging = paginator.paginate_queryset(question_list, request)
        
        question_serializer = QuestionsSerializers(question_paging, many=True)
        
        return paginator.get_paginated_response({
            'quiz_id': question_serializer.data
        })