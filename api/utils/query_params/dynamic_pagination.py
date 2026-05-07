from rest_framework.pagination import PageNumberPagination

class DynamicPagination(PageNumberPagination):
    page_size_query_param = 'size' 
    max_page_size = 100