from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser

from .serializers import QuizSerializers, QuestionsSerializers, CreateQuizSerializer
from .models import Quiz, Questions

# Create your views here.
class QuizManager(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    
    queryset = Quiz.objects.prefetch_related('quiz_id').all()
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateQuizSerializer
        return QuizSerializers

    # 생성
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            quiz = serializer.save()
            response_serializer = QuizSerializers(quiz)
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 수정
    def update(self, request, *args, **kwargs):
        quiz = self.get_object()
        quiz_serializer = self.get_serializer(quiz, data=request.data)
        
        if quiz_serializer.is_valid():
            # 퀴즈 업데이트
            quiz = quiz_serializer.save()
            
            # 문제 업데이트
            question_data = request.data.get('quiz_id', [])
            for question_info in question_data:
                question = Questions.objects.get(id = question_info.get('id'))
                question_serializer = QuestionsSerializers(question, data = question_info, partial=True)
                
                if question_serializer.is_valid():
                    question_serializer.save()
            
            response_serializer = QuizSerializers(quiz)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def destroy(self, *args, **kwargs):
        quiz = self.get_object()
        quiz.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)