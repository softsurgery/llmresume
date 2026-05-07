from drf_spectacular.utils import OpenApiParameter

list_parameters = [
    OpenApiParameter(name="filter", type=str, location=OpenApiParameter.QUERY),
    OpenApiParameter(name="search", type=str, location=OpenApiParameter.QUERY),
    OpenApiParameter(name="sort", type=str, location=OpenApiParameter.QUERY),
]

paginated_parameters = [
    OpenApiParameter(name="filter", type=str, location=OpenApiParameter.QUERY),
    OpenApiParameter(name="search", type=str, location=OpenApiParameter.QUERY),
    OpenApiParameter(name="sort", type=str, location=OpenApiParameter.QUERY),
    OpenApiParameter(name="page", type=int, location=OpenApiParameter.QUERY, default=1),
    OpenApiParameter(name="size", type=int, location=OpenApiParameter.QUERY, default=10),
]