from rest_framework import serializers
from .models import Quiz, Questions

class QuestionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id','title', 'answer', 'correct_answer')

class QuizSerializers(serializers.ModelSerializer):
    quiz_id = QuestionsSerializers(many = True, read_only = True)
    
    class Meta:
        model = Quiz
        fields = ('id','title', 'questions_count','quiz_id')

class CreateQuizSerializer(serializers.Serializer):
    title = serializers.CharField()
    questions = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField()
        )
    )

    def create(self, validated_data):
        quiz = Quiz.objects.create(title=validated_data['title'])

        questions = [
            Questions(quiz=quiz, title=question['title'], answer=question['answer'], correct_answer=question['correct_answer'])
            for question in validated_data['questions']
        ]
        Questions.objects.bulk_create(questions)

        return quiz