from rest_framework.pagination import PageNumberPagination


class CustomizablePageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 2000


class LargeResultsSetPagination(CustomizablePageNumberPagination):
    page_size = 100


class StandardResultsSetPagination(CustomizablePageNumberPagination):
    page_size = 50


class SmallResultsSetPagination(CustomizablePageNumberPagination):
    page_size = 10


class TinyResultsSetPagination(CustomizablePageNumberPagination):
    page_size = 5
