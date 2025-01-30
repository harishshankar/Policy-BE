from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    def __init__(self, status_code=None):
        if status_code is not None:
            self.status_code = status_code

    def get_full_details(self):
        return {
            "status": self.status_code,
            "data": None,
        }


class RequestError(CustomAPIException):
    pass


class InternalError(CustomAPIException):
    pass


class ApiResponse:

    @staticmethod
    def success(data, status=status.HTTP_200_OK, additional_data=None, request=None):
        response = {
            "status": status,
            "data": data,
        }
        if request:
            page_data = {
                "page": request.query_params.get("page", "1"),
                "page_size": request.query_params.get("page_size", "20"),
            }
            for key, value in page_data.items():
                if not value.isnumeric():
                    return ApiResponse.request_error(
                        data=f"Invalid {key}, must be numeric'"
                    )

            page = int(page_data["page"])
            page_size = int(page_data["page_size"])

            total_count = request.count if hasattr(request, "count") else len(data)

            total_pages = (total_count // page_size) + (
                1 if total_count % page_size else 0
            )

            paginator = Paginator(data, page_size)
            try:
                info = paginator.page(page)
            except EmptyPage:
                info = paginator.page(paginator.num_pages)
            except ZeroDivisionError:
                return ApiResponse.request_error(data=f"page cannot be zero.")

            data = {
                "page_details": {
                    "count": total_count,
                    "total_page": total_pages,
                    "current_page": page,
                    "entries_in_this_page": len(info),
                    "has_previous_page": page > 1,
                    "has_next_page": page < total_pages,
                    "sort_by": additional_data.get("sort_by", None),
                },
                "data": list(info),
            }
            response["data"] = data
        return Response(response, status=status)

    @staticmethod
    def request_error(data, status_code=status.HTTP_400_BAD_REQUEST):
        raise RequestError(detail=data, status_code=status_code)

    @staticmethod
    def internal_error(
        data,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        raise InternalError(detail=data, status_code=status_code)
