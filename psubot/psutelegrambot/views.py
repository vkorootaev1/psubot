import asyncio
import sys

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import UserNotFoundQuestionFilter
from .models import Question, UserNotFoundQuestion, TelegramUser
from .pagination import UserNotFoundQuestionPagination
from .serializers import QuestionSerializer, TreeSerializer, ListOfRootsSerializer, UserNotFoundQuestionSerializer

sys.path.append("C:\Course\psubot")
from telegram.functions import replyUserMessage
from telegram.functions import massMailingTelegramUsers


# Представление для получения дерева по id его корня
class TreeApiView(generics.ListAPIView):
    serializer_class = TreeSerializer
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        questions = Question.objects.filter(id=pk, parent_id=None)
        if questions:
            return questions
        else:
            raise NotFound()


# Представление для создания, обновления, удаления отдельных вершин дерева
class QuestionApiView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Представление для получения списка корневых вопросов
class ListOfRoots(generics.ListAPIView):
    serializer_class = ListOfRootsSerializer
    queryset = Question.objects.filter(parent_id=None).order_by('-id')


# Представление для вопросов пользователей
class UserNotFoundQuestionView(viewsets.ModelViewSet):
    queryset = UserNotFoundQuestion.objects.all().order_by('-question_time')
    serializer_class = UserNotFoundQuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserNotFoundQuestionFilter
    pagination_class = UserNotFoundQuestionPagination


# Представление ответа пользователю, что его вопрос занесен в базу данных
class replyUserView(APIView):
    def post(self, request):
        asyncio.run(
            replyUserMessage(request.data["first_name"], request.data["user_id"], request.data["message_id"],
                             request.data["language_code"]))
        return Response(status=status.HTTP_200_OK)


# Массовая рассылка пользователям
class MassMailingView(APIView):
    def post(self, request):
        all_telegram_users = TelegramUser.objects.all()
        allUsersId = []
        for telegram_user in all_telegram_users:
            allUsersId.append({"id": telegram_user.user_id, "language_code": telegram_user.language_code})
        asyncio.run(
            massMailingTelegramUsers(request.data['text_message_ru'], request.data['text_message_en'], allUsersId))
        return Response(status=status.HTTP_200_OK)
