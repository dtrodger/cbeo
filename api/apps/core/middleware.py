"""
Core app HTTP middleware
"""
import logging

from django.conf import settings
import copy


log = logging.getLogger(__name__)


class LoggingMiddleware:
    """
    HTTP middleware to log requests
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.REQUEST_LOGGING:
            log.debug(f"request host {request.get_host()}")
            log.debug(f"request path {request.path}")
            log.debug(f"request method {request.method}")
            headers = copy.deepcopy(dict(request.headers))
            if headers.get("Authorization"):
                del headers["Authorization"]

            log.debug(f"request headers {headers}")

        return self.get_response(request)
