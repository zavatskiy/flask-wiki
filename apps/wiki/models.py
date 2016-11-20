# coding=utf-8

from sqlalchemy.sql.expression import text
from core.database import db


class WikiPageVersion(db.Model):
    __tablename__ = 'wiki_page_version'

    (
        STATUS_NOT_CURRENT,
        STATUS_CURRENT,
    ) = range(2)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    status = db.Column(db.Integer, default=STATUS_CURRENT, index=True)
    wiki_page_id = db.Column(
        db.Integer, db.ForeignKey('wiki_page.id'), index=True
    )

    def __repr__(self):
        return '<WikiPageVersion %s>' % self.id

    @classmethod
    def condition_status_current(cls):
        return cls.status == WikiPage.STATUS_CURRENT

    @classmethod
    def condition_status_not_current(cls):
        return cls.status == WikiPage.STATUS_NOT_CURRENT


class WikiPage(db.Model):
    __tablename__ = 'wiki_page'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    versions = db.relationship("WikiPageVersion")

    def __repr__(self):
        return '<WikiPage %s>' % self.id

    def get_current(self):
        return next(iter([
            version for version in self.versions
            if version.status == WikiPageVersion.STATUS_CURRENT
        ]), None)
