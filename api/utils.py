"""
Utils
"""
import os

from django.http import JsonResponse, HttpResponse


class SuccessJsonResponse(JsonResponse):
    """HTTP 200 success JSON response"""

    def __init__(self, *args, **kwargs):
        if not args:
            args = ({},)

        super().__init__(status=200, *args, **kwargs)


class ErrorJsonResponse(JsonResponse):
    """HTTP 400 server error JSON response"""

    def __init__(self, data, *args, **kwargs):
        if not args:
            args = ({},)

        super().__init__(status=400, *args, **kwargs)


class UnauthorizedHTTPResponse(HttpResponse):
    """HTTP 403 Unauthorized response"""

    def __init__(self, *args, **kwargs):
        super().__init__(status=403, *args, **kwargs)


class UnauthorizedJsonResponse(JsonResponse):
    """HTTP 403 Unauthorized JSON response"""

    def __init__(self, *args, **kwargs):
        if not args:
            args = ({},)

        super().__init__(status=403, *args, **kwargs)


class ServiceUnavailableJsonResponse(JsonResponse):
    """HTTP 500 server error JSON response"""

    def __init__(self, data, *args, **kwargs):
        if not args:
            args = ({},)

        super().__init__(status=503, *args, **kwargs)


class ServiceUnavailableHTTPResponse(HttpResponse):
    """HTTP 503 service unavailable response"""

    def __init__(self, *args, **kwargs):
        super().__init__(status=503, *args, **kwargs)


def env_file_path():
    return os.path.join(os.path.dirname(__file__), "..", "env", ".env.local")


def set_env_var(key, value, is_list=False, is_bool=False, is_int=False, exce=True):
    if exce:
        if os.environ.get(key):
            raise Exception(f"Environment {key} variable already exists")

    if is_list:
        value = value.split(",")
    if is_int:
        value = int(value)
    elif is_bool:
        lower_val = value.lower()
        if lower_val in ["t", "true"]:
            value = True
        elif lower_val in ["f", "false"]:
            value = False

    else:
        os.environ[key] = value


def deployed():
    """
    Am I deployed?
    """

    return get_env_var("ENVIRONMENT") != "local"


def get_env_var(
    key, default=None, is_list=False, is_bool=False, is_int=False, exce=True
):
    value = os.environ.get(key, default)
    if exce and not value:
        raise Exception(f"Missing required environment variable {key}")

    if is_list:
        value = value.split(",")
    if is_int:
        value = int(value)
    elif is_bool:
        lower_val = value.lower()
        if lower_val in ["t", "true"]:
            value = True
        elif lower_val in ["f", "false"]:
            value = False

    elif value == "NONE":
        value = None

    return value
