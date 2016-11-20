# coding=utf-8

import hmac
import json
import requests

from flask import current_app


def post(url, data):
    data = json.dumps(data)
    content_md5 = hmac.new(current_app.config['API_KEY'], data).hexdigest()
    return requests.post(
        url, data=data, headers={
            'content-type': 'application/json',
            'x-content-md5': content_md5
        }
    )
