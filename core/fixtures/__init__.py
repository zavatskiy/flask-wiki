# coding=utf-8

from fixture import SQLAlchemyFixture
from fixture.style import NamedDataStyle

from core.database import db
from wiki.models import WikiPage, WikiPageVersion
from fixture_wiki import WikiPageData, WikiPageVersionData


models_map = {
    'WikiPage': WikiPage,
    'WikiPageVersion': WikiPageVersion,
}

dbfixture = SQLAlchemyFixture(
    env=models_map,
    style=NamedDataStyle(),
    engine=db.engine
)

fixtures_data = (
    WikiPageData,
    WikiPageVersionData,
)


def fixtures_install(app, *args):
    data = dbfixture.data(*args)
    data.setup()
