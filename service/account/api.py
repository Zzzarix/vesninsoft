from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from rest_framework import status, serializers
from .backend import *

import traceback


class CreatePayslipsSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_blank=False)

@api_view(["POST", "GET"])
def apiCreatePayslips(request: Request):
    try:
        if request.method == 'GET':
            return HttpResponseRedirect('/account')
        if not request.data:
             return HttpResponse(content=f'Does not passed data', status=status.HTTP_400_BAD_REQUEST)
        content = request.data.get('content', None)
        if not content:
            return HttpResponse(content=f'Does not passed required field: content', status=status.HTTP_400_BAD_REQUEST)
        try:
            parse_payslip_registry(content)
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Exception as exc:
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            return HttpResponse(content=f'Internal server error: { traceback.format_exception(type(exc), exc, exc.__traceback__)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as exc:
            return HttpResponse(content=f'Internal server error: { traceback.format_exception(type(exc), exc, exc.__traceback__)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    