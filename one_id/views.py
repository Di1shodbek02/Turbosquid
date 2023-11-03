from django.shortcuts import redirect
from dotenv import load_dotenv
from rest_framework.generics import GenericAPIView
import os
import requests

load_dotenv()
BASE_URL = 'https://sso.egov.uz/sso/oauth/Authorization.do'


class OneIDAuthAPIView(GenericAPIView):
    permission_classes = ()

    def get(self, request):
        response_type = 'one_code'
        client_id = os.getenv('CLIENT_ID')
        redirect_url = 'http://127.0.0.1:8000/code'
        scope = 'testScope'
        state = 'testState'

        return redirect(f'{BASE_URL}?response_type={response_type}&client_id={client_id}&redirect_url={redirect_url}'
                        f'&Scope{scope}&State={state}')
