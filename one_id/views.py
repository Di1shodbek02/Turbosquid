from django.shortcuts import redirect
from django.views import View
from dotenv import load_dotenv
from rest_framework.generics import GenericAPIView
import os
import requests
from rest_framework.response import Response

load_dotenv()
BASE_URL = 'https://sso.egov.uz/sso/oauth/Authorization.do'


class OneIDAuthAPIView(GenericAPIView):
    permission_classes = ()

    def get(self, request):
        response_type = 'one_code'
        client_id = os.getenv('CLIENT_ID')
        redirect_uri = 'http://127.0.0.1:8000/oneid/code'
        scope = 'testScope'
        state = 'testState'

        return redirect(f'{BASE_URL}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}')


class OneIDCodeAPIVIEW(GenericAPIView):
    permission_classes = ()

    def get(self, request):
        code = request.GET.get('code')
        grant_type = 'one_authorization_code'
        client_id = os.getenv('CLIENT_ID')
        secret_key = os.getenv('SECRET_KEY')
        redirect_uri = 'http://127.0.0.1:8000/oneid/code'

        response = requests.post(BASE_URL, params={
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': secret_key,
            'redirect_uri': redirect_uri,
            'code': code
        })

        return Response(response.json())
