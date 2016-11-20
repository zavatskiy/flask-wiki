# coding=utf-8

import json

from flask_restless import url_for

from core.tests.base import TestCase
from core.fixtures.fixture_wiki import WikiPageData, WikiPageVersionData
from wiki.models import WikiPage, WikiPageVersion


class TestWikiPage(TestCase):

    datasets = [WikiPageData, WikiPageVersionData]

    def setUp(self):
        super(TestWikiPage, self).setUp()
        self.wiki_page01 = self.data.WikiPageData.wiki_page01
        self.wiki_page_version01 = (
            self.data.WikiPageVersionData.wiki_page_version01
        )
        self.wiki_page_version02 = (
            self.data.WikiPageVersionData.wiki_page_version02
        )

    def test_wiki_page_list(self):
        response = self.client.get(url_for(WikiPage))
        self.assert_200(response)

    def test_wiki_page(self):
        response = self.client.get(
            url_for(WikiPage, instid=self.wiki_page01.id)
        )
        self.assert_200(response)
        self.assertEqual(response.json['id'], self.wiki_page01.id)
        self.assertEqual(len(response.json['versions']), 2)

    def test_wiki_page_current(self):
        response = self.client.post(
            url_for(WikiPage),
            headers=[('Content-Type', 'application/json')],
            data=json.dumps(dict(title='TITLE', text='TEXT')),
        )
        wiki_page_id = response.json['id']
        response = self.client.get(
            url_for(WikiPageVersion, q=json.dumps({
                "filters": [
                    {"name": "wiki_page_id", "op": "eq", "val": wiki_page_id},
                    {
                        "name": "status", "op": "eq", "val":
                        WikiPageVersion.STATUS_CURRENT
                    }
                ]
            }))
        )
        self.assert_200(response)
        self.assertEqual(
            response.json['objects'][0]['status'],
            WikiPageVersion.STATUS_CURRENT
        )

    def test_wiki_page_version(self):
        response = self.client.get(
            url_for(WikiPageVersion, instid=self.wiki_page_version01.id)
        )
        self.assert_200(response)
        self.assertEqual(response.json['id'], self.wiki_page_version01.id)

    def test_wiki_page_version_change_status(self):
        response = self.client.patch(
            url_for(WikiPageVersion, instid=self.wiki_page_version01.id),
            headers=[('Content-Type', 'application/json')],
            data=json.dumps(dict(status=WikiPageVersion.STATUS_NOT_CURRENT))
        )
        self.assert_200(response)
        self.assertEqual(
            response.json['status'], WikiPageVersion.STATUS_NOT_CURRENT
        )

    def test_wiki_page_add(self):
        response = self.client.post(
            url_for(WikiPage),
            headers=[('Content-Type', 'application/json')],
            data=json.dumps(dict(title='TITLE', text='TEXT')),
        )
        self.assertStatus(response, 201)
        self.assertEqual(response.json['versions'][0]['title'], 'TITLE')
        self.assertEqual(response.json['versions'][0]['text'], 'TEXT')
        self.assertEqual(
            response.json['versions'][0]['status'],
            WikiPageVersion.STATUS_CURRENT
        )
