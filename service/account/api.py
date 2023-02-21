from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpRequest
from rest_framework import status, serializers
from .backend import *

import traceback


class CreatePayslipsSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_blank=False)

@api_view(["POST", "GET"])
def apiCreatePayslips(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseRedirect('/account')
    data = request.POST.copy()
    content = data.get('content', None)
    if not content:
        return Response(f'Does not passed required field: content, {request.body}', status=status.HTTP_400_BAD_REQUEST)
    try:
        parse_payslip_registry(content)
        return Response(status=status.HTTP_201_CREATED)
    except Exception as exc:
        return Response(data=f'Internal server error: { traceback.format_exception(type(exc), exc, exc.__traceback__)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR, template_name=None)
