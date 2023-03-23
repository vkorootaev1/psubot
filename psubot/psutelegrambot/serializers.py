from rest_framework import serializers
from .models import Question
from rest_framework_recursive.fields import RecursiveField


class TreeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Question
        fields = ('id', 'parent_id', 'text_ru', 'text_en', 'children')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'parent_id', 'text_ru', 'text_en')



