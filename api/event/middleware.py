import logging

import urllib.parse
from orjson import orjson
from orjson.orjson import JSONDecodeError
from django.http.multipartparser import MultiPartParser
from event.models import Log

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/api/v1/admin"):
            self.log(request=request, response=response)
        return response

    @classmethod
    def _parse_data(cls, request, response) -> dict | None:
        user = None

        if request.user.is_authenticated:
            user = request.user

        content_type = request.META.get("CONTENT_TYPE", "")
        if not content_type.startswith("multipart/"):
            try:
                request_data = orjson.loads(request.body.decode("utf-8"))
            except JSONDecodeError:
                request_data = request.body.decode("utf-8")
        else:
            data = MultiPartParser(request.META, request, request.upload_handlers)
            request_data, files = data.parse()

        try:
            response_data = orjson.loads(response.content.decode("utf-8"))
        except JSONDecodeError:
            response_data = response.content.decode("utf-8")

        query_params = urllib.parse.parse_qs(request.META.get("QUERY_STRING", ""))  # noqa
        # simplified_query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

        return {
            "user": user,
            "request_data": request_data,
            "response_data": response_data,
            "user_agent": str(request.META.get("HTTP_USER_AGENT")),
            "ip_address": str(request.META.get("REMOTE_ADDR")),
            "path": str(request.META.get("PATH_INFO")),
            "http_method": str(request.META.get("REQUEST_METHOD")),
            # "query_params": simplified_query_params,
            "status_code": response.status_code,
        }

    @classmethod
    def log(cls, request, response):
        data = cls._parse_data(request, response)
        if data is not None:
            Log.objects.create(**data)
