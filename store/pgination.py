from rest_framework.pagination import PageNumberPagination


class DefaultPgaination(PageNumberPagination):
    page_size = 10