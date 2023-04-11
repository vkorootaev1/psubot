from rest_framework.pagination import PageNumberPagination


class UserNotFoundQuestionPagination(PageNumberPagination):
    # Поменять на 50-100
    page_size = 20
    page_size_query_param = 'page_size'