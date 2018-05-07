""" sets base db model for applciation """
from flask import current_app
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, text
from .database_model import DatabaseModel
from .json_model import JsonModel


class BaseModel(DatabaseModel, JsonModel):
    """ Adds usefull custom attributes for applciation use """

    __abstract__ = True
    id = Column(Integer, primary_key=True)
    updated_at = Column(DateTime)
    created_at = Column(DateTime)

    def __init__(self):
        DatabaseModel.__init__(self)

    @classmethod
    def where_id(cls, id):
        """ Get db model by id """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def paginate(cls, limit, page_number=0) -> list:
        """ Return [models] by page_number based on limit """
        # workaround flask-sqlalchemy/issues/516
        offset = page_number * limit
        sql = text('SELECT * FROM %s LIMIT :li OFFSET :o'
                   % (cls.__tablename__))
        result = cls.db.engine.execute(
            sql, li=limit, o=offset)
        result_keys = result.keys()
        result_models = []
        for row in result:
            model = cls()
            key_count = 0
            for key in result_keys:
                setattr(model, key, row[key_count])
                key_count = key_count + 1
            result_models.append(model)
        return result_models

    @classmethod
    def paginate_max_pages(cls, limit) -> int:
        """ Return total max pages created by limit """
        row_count = cls.query.count()
        if isinstance(row_count, int):
            return int(row_count / limit)
        return None

    @staticmethod
    def paginate_links(base_link, current_page, limit, max_pages) -> dict:
        """ Return JSON paginate links """
        max_pages = max_pages - 1 if max_pages > 0 else max_pages
        base_link = '/%s' % (base_link.strip("/"))
        self_page = current_page
        prev = current_page - 1 if current_page is not 0 else None
        prev_link = '%s/page/%s/%s' % (base_link, prev, limit) if \
            prev is not None else None
        next = current_page + 1 if current_page < max_pages else None
        next_link = '%s/page/%s/%s' % (base_link, next, limit) if \
            next is not None else None
        first = 0
        last = max_pages
        return {
            'self': '%s/page/%s/%s' % (base_link, self_page, limit),
            'prev': prev_link,
            'next': next_link,
            'first': '%s/page/%s/%s' % (base_link, first, limit),
            'last': '%s/page/%s/%s' % (base_link, last, limit),
        }

    def exists(self):
        """ Checks if item already exists in database """
        self_object = self.query.filter_by(id=self.id).first()
        if self_object is None:
            return False
        return True

    def updated(self):
        """ Update updated_at timestamp """
        self.updated_at = datetime.utcnow()
        self.save()

    def delete(self):
        """ Easy delete for db models """
        try:
            if self.exists() is False:
                return None
            self.db.session.delete(self)
            self.db.session.commit()
        except (Exception, BaseException) as error:
            # fail silently
            return None

    def save(self):
        """ Easy save(insert or update) for db models """
        try:
            if self.exists() is False:
                self.db.session.add(self)
            # self.db.session.merge(self)
            self.db.session.commit()
        except (Exception, BaseException) as error:
            if current_app.config['DEBUG']:
                raise error
            return None
