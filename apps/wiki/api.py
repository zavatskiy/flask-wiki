# coding=utf-8

from flask_restless import ProcessingException
from core.restless import check_access
from wiki.models import WikiPage, WikiPageVersion


def prepare_new_page(data=None, **kwargs):
    data['versions'] = [{
        'title': data.pop('title'),
        'text': data.pop('text'),
    }]


def prepare_new_version(data=None, **kwargs):
    wiki_page = WikiPage.query.get(data.get('wiki_page_id'))
    if not wiki_page:
        raise ProcessingException(code=404)
    current = wiki_page.get_current()
    if current:
        current.status = WikiPageVersion.STATUS_NOT_CURRENT


wiki_pages = {
    'model': WikiPage,
    'primary_key': 'id',
    'methods': ['GET', 'POST'],
    'include_columns': [
        'id', 'created', 'modified', 'versions', 'versions.id',
        'versions.title', 'versions.text', 'versions.status'
    ],
    'results_per_page': 20,
    'preprocessors': dict(GET_MANY=[check_access],
                          GET_SINGLE=[check_access],
                          POST=[check_access, prepare_new_page]),
}


wiki_page_versions = {
    'model': WikiPageVersion,
    'primary_key': 'id',
    'methods': ['GET', 'POST', 'PATCH'],
    'include_columns': ['id', 'title', 'text', 'status'],
    'results_per_page': 20,
    'preprocessors': dict(GET_SINGLE=[check_access],
                          POST=[check_access, prepare_new_version]),
}
