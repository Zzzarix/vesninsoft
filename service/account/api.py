from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from rest_framework import status, serializers
from .backend import *

import traceback


class CreatePayslipsSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_blank=False)

@api_view(["POST", "GET"])
def apiCreatePayslips(request: HttpRequest):
    try:
        if request.method == 'GET':
            return HttpResponseRedirect('/account')
        data = request.POST.copy()
        content = data.get('content', None)
        if not content:
            return HttpResponse(content=f'Does not passed required field: content, {request.__dict__.__str__()}', status=status.HTTP_400_BAD_REQUEST)
        try:
            parse_payslip_registry(content)
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Exception as exc:
            return HttpResponse(content=f'Internal server error: { traceback.format_exception(type(exc), exc, exc.__traceback__)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR, template_name=None)
    except Exception as exc:
            return HttpResponse(content=f'Internal server error: { traceback.format_exception(type(exc), exc, exc.__traceback__)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR, template_name=None)
    