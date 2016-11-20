# coding=utf-8

from fixture import DataSet


class WikiPageVersionData(DataSet):

    class wiki_page_version01:
        title = 'TITLE01'
        text = 'TEXT01'
        status = 1

    class wiki_page_version02:
        title = 'TITLE02'
        text = 'TEXT02'
        status = 0


class WikiPageData(DataSet):

    class wiki_page01:
        versions = [
            WikiPageVersionData.wiki_page_version01,
            WikiPageVersionData.wiki_page_version02
        ]
