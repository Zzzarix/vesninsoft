from rest_framework.decorators import api_view
from rest_framework.request import Request
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from api.backend import *

import traceback


@api_view(["POST", "GET"])
def apiSalaryReport(request: Request):
    try:
        if request.method == 'GET':
            return HttpResponseRedirect('/account')
        if not request.data:
             return HttpResponse(content=f'Does not passed data', status=status.HTTP_400_BAD_REQUEST)
        content_file: InMemoryUploadedFile = request.data.get('content', None)
        if not content_file:
            return HttpResponse(content=f'Does not passed required field: content', status=status.HTTP_400_BAD_REQUEST)
        try:
            parse_payslip_registry(content_file.read())
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Exception as exc:
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            return HttpResponse(content=f'Internal server error: { traceback.format_exception(type(exc), exc, exc.__traceback__)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as exc:
            return HttpResponse(content=f'Internal server error: { request._data}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST", "GET"])
def apiAddOrg(request: Request):
    try:
        if request.method == 'GET':
            return HttpResponseRedirect('/account')
        if not request.data:
             return HttpResponse(content=f'Does not passed data', status=status.HTTP_400_BAD_REQUEST)
        content_file: InMemoryUploadedFile = request.data.get('content', None)
        if not content_file:
            return HttpResponse(content=f'Does not passed required field: content', status=status.HTTP_400_BAD_REQUEST)
        try:
            _status = parse_org(content_file.read())
            if _status == AddOrgStatus.ALREADY_LINKED_OTHER_COMPANY:
                return HttpResponse(content=f'To this user already linked the company', status=status.HTTP_400_BAD_REQUEST)
            elif _status == AddOrgStatus.INCORRECT_USER:
                return HttpResponse(content=f'Invalid user credentials provided', status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Exception as exc:
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            return HttpResponse(content=f'Incorrect content field', status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
            return HttpResponse(content=f'Internal server error: { request._data}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
