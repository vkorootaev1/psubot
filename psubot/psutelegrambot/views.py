from rest_framework import generics, mixins, viewsets
from rest_framework.exceptions import NotFound
from .models import Question
from .serializers import QuestionSerializer, TreeSerializer, ListOfRootsSerializer


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
    queryset = Question.objects.filter(parent_id=None).order_by('id')


