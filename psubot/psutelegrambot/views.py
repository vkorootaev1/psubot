from rest_framework import generics, mixins, viewsets
from rest_framework.exceptions import NotFound
from .models import Question
from .serializers import QuestionSerializer, TreeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


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


class QuestionApiView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class GetLastIdApiView(APIView):

    def get(self, request, format=None):
        last_row = Question.objects.latest('id')
        return Response({'last_id': last_row.id})
