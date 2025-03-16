from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import random
import itertools
import copy

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from quiz_board.serializers import QuestionsBoardSerializers

from quiz_board import utils
from quiz_manager.models import Questions, Quiz
from .models import History

# Create your views here.
class Exam(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_session_key(self, user_id, quiz_id):
        return f"exam_{user_id}_{quiz_id}"
    
    # 시험 생성
    @action(detail = True, methods = ['post'], url_path='exam-start')
    def exam_start(self, request, pk):
        session_key = self.get_session_key(request.user, pk)
        if session_key in request.session:
            return Response(request.session[session_key])
        
        quiz = Quiz.objects.get(id = pk)
        questions = list(Questions.objects.filter(quiz = pk))
        setting = utils.get_board_setting()

        # 질문 개수가 많을경우
        if len(questions) >= quiz.questions_count:
            if setting.question_random:
                question_list = random.sample(questions, quiz.questions_count)
            else:
                question_list = questions[:quiz.questions_count]
        else:
            #부족한 개수
            shortage = quiz.questions_count - len(questions)
            if setting.question_random:
                random_question = random.choices(questions, k=shortage)
                question_list = questions + random_question
                random.shuffle(question_list)
            else:
                # 랜덤이 아닐경우 순서대로 반복
                question_list = list(itertools.islice(itertools.cycle(questions), quiz.questions_count))
                
        # 선택지 랜덤 설정
        if setting.choice_random:
            for idx, question in enumerate(question_list):
                question_copy = copy.deepcopy(question)
                answer = question_copy.answer[:]
                random.shuffle(answer)
                question_copy.answer = answer
                question_list[idx] = question_copy
        
        question_serializer = QuestionsBoardSerializers(question_list, many=True).data
        request.session['questions'] = question_serializer
        return Response({
            "message": "start quiz",
            "questions": request.session['questions']
        })
    
    # 시험 페이지
    @action(detail = True, methods = ['get'], url_path='exam-page')
    def exam_page(self, request, page=1, pk = None):
        setting = utils.get_board_setting()
        quiz_questions = request.session.get('questions', [])

        paginator = Paginator(quiz_questions, setting.question_paging)
        question_page = paginator.get_page(page)
        
        now_page = request.GET.get('page', 1)
        return Response({
            "page": int(now_page),
            "total_pages": paginator.num_pages,
            "questions": question_page.object_list
        })
        
    # 시험 결과 제출
    @action(detail = True, methods = ['post'], url_path='exam-submit')
    def exam_submit(self, request, pk = None):
        quiz = Quiz.objects.get(id = pk)
        submit_answers = request.data.get('answers', [])
        questions = request.session.get('questions', [])
        
        if not submit_answers:
            return Response({"message": "No answers submitted."})
        if not questions:
            return Response({"message": "Session close"})
        
        questions_count = len(questions)
        score = 0
        
        for answer in submit_answers:
            question_id = questions[int(answer.get('question_num'))-1]["id"]
            user_answer = answer.get('user_answer')
            question = Questions.objects.get(id = question_id)
            
            if not user_answer:
                continue
            if user_answer == question.correct_answer:
                score += 1
                
        save_history = History.objects.create(
            user_id = request.user,
            quiz_id = quiz,
            question_count = questions_count,
            score = score
        )
        
        return Response({
            "message" : "submit success",
            "title" : Quiz.objects.get(id = pk).title,
            "question_count" : questions_count,
            "score" : score
        })