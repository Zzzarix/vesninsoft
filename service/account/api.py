from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status, serializers
from .backend import *
import logging

import traceback


class CreatePayslipsSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_blank=False)

@api_view(["POST", "GET"])
def apiCreatePayslips(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/account')
    data = request.POST.copy()
    logging.info(f"{data}, {request.headers}")
    content = data.get('content', None)
    if not content:
        return Response('Does not passed required field: content', status=status.HTTP_400_BAD_REQUEST)
    try:
        parse_payslip_registry(content)
        return Response(status=status.HTTP_201_CREATED)
    except Exception as exc:
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=__file__)
        return Response('Internal server error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
