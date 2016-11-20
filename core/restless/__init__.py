# coding=utf-8

import hmac

from flask import request, current_app
from flask_restless import APIManager, ProcessingException


def check_api_key(*args, **kwargs):
    customer_hmac = str(request.headers.get('x-content-md5'))
    server_hmac = hmac.new(
        current_app.config['API_KEY'], str(request.data)
    ).hexdigest()
    if not hmac.compare_digest(server_hmac, customer_hmac):
        raise ProcessingException(description='Not authenticated!', code=401)


def check_access(*args, **kwargs):
    #if not current_user.is_superuser:
        #raise ProcessingException(description='Not authenticated!', code=401)
    pass


apimanager = APIManager()
