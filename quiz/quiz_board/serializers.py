from rest_framework import serializers

from quiz_manager.models import Quiz, Questions
from .models import BoardSetting

class SettingSerializers(serializers.ModelSerializer):
    class Meta:
        model = BoardSetting
        fields = ('quiz_paging', 'question_paging', 'question_random', 'choice_random')

class QuestionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id','title', 'answer') 

class QuizSerializers(serializers.ModelSerializer):
    quiz_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ('id','title', 'questions_count','quiz_id')
        
    def get_quiz_id(self, obj):
        if self.context.get('view').action == 'retrieve':
            return QuestionsSerializers(obj.quiz_id.all(), many=True).data
        return []