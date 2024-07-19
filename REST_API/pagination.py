from rest_framework.pagination import (
    CursorPagination,
    LimitOffsetPagination,
    PageNumberPagination,
)


class ParkingSpacePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class VehicleInfoPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20


class ParkingDetailsPagination(CursorPagination):
    page_size = 10
    ordering = "created_at"
