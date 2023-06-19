"""
Core app views
"""
import sentry_sdk
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from apps.core.models import Pitch


def handler404(request, exception=None):
    """
    404 error handler view
    """

    return TemplateResponse(request, "public/not_found.html")


def handler500(request, exception=None):
    """
    500 error handler view
    """

    if exception:
        sentry_sdk.capture_exception(exception)

    return TemplateResponse(request, "public/server_error.html")


@method_decorator(csrf_exempt, name="dispatch")
class StatusView(APIView):
    """
    StatusView endpoint
    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """
        GET request handler
        """
        return Response({}, status=status.HTTP_200_OK)


class PitchUpload(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        pitch_file = request.FILES.get("file")
        pitch_file_name = request.POST.get("file_name")
        if not pitch_file:
            return Response({"missing_file": True}, status=status.HTTP_400_BAD_REQUEST)
        if not pitch_file_name:
            return Response({"missing_file_name": True}, status=status.HTTP_400_BAD_REQUEST)

        message_type_counts = {
            "symbol_clear_message_count": 0,
            "add_order_message_count": 0,
            "modify_order_message_count": 0,
            "execute_order_message_count": 0,
            "cancel_order_message_count": 0,
            "trade_message_count": 0,
            "trade_break_message_count": 0,
            "trading_status_message_count": 0,
            "auction_update_message_count": 0,
            "auction_summary_message_count": 0,
            "retail_price_improvement_message_count": 0,
        }
        invalid_messages = []
        for line in pitch_file:
            try:
                line_data = line.decode('utf-8').strip()
                message_type = line_data[9:10]
                if message_type == "s":
                    message_type_counts["symbol_clear_message_count"] += 1
                elif message_type in ["A", "d"]:
                    message_type_counts["add_order_message_count"] += 1
                elif message_type == "E":
                    message_type_counts["execute_order_message_count"] += 1
                elif message_type == "X":
                    message_type_counts["cancel_order_message_count"] += 1
                elif message_type in ["P", "r"]:
                    message_type_counts["trade_message_count"] += 1
                elif message_type == "B":
                    message_type_counts["trade_break_message_count"] += 1
                elif message_type == "H":
                    message_type_counts["trading_status_message_count"] += 1
                elif message_type == "I":
                    message_type_counts["auction_update_message_count"] += 1
                elif message_type == "J":
                    message_type_counts["auction_summary_message_count"] += 1
                elif message_type == "R":
                    message_type_counts["retail_price_improvement_message_count"] += 1
                else:
                    invalid_messages.append(line_data)
            except:
                invalid_messages.append(line_data)

        if invalid_messages:
            return Response({"invalid_message": invalid_messages}, status=status.HTTP_400_BAD_REQUEST)
        else:
            pitch = Pitch.objects.create(
                **message_type_counts,
                file=pitch_file,
                file_name=pitch_file_name
            )
            return Response(pitch.serialize(serializer_fields=[
                "id",
                "file_name",
                "created",
                "symbol_clear_message_count",
                "add_order_message_count",
                "modify_order_message_count",
                "execute_order_message_count",
                "trade_message_count",
                "trade_break_message_count",
                "cancel_order_message_count",
                "trading_status_message_count",
                "auction_update_message_count",
                "auction_summary_message_count",
                "retail_price_improvement_message_count"
            ]), status=status.HTTP_200_OK)


class PitchModelView(ModelViewSet):
    """
    Pitch model view
    """

    http_method_names = ["get", "list"]
    queryset = Pitch.objects.order_by("-created")
    serializer_class = Pitch.serializer()
    permission_class = [AllowAny]
