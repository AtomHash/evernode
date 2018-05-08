"""
    Used to help pagination of base_model results
"""
from ..classes import Security
from sqlalchemy import text


class Paginate:
    """ Make pagination easy """

    __filters = []
    model = None
    limit = None
    max_pages = None

    def __init__(self, model, limit):
        self.__filters = []
        self.model = model
        self.limit = limit
        self.max_pages = self.__total_pages()

    def __total_pages(self) -> int:
        """ Return max pages created by limit """
        row_count = self.model.query.count()
        if isinstance(row_count, int):
            return int(row_count / self.limit)
        return None

    def __filter_query(self) -> str:
        """ Generate a WHERE/AND string for SQL"""
        filter_query = 'WHERE %s'
        bind_values = {}
        if not self.__filters:
            return None
        for filter in self.__filters:
            bind = {
                'name': Security.random_string(5),
                'value': filter['value']}
            filter_str = '%s %s :%s' % \
                (filter['column'], filter['operator'], bind['name'])
            bind_values[bind['name']] = bind['value']
            filter_query = filter_query % (filter_str + ' AND %s')
        return {
            'query': filter_query.replace(' AND %s', ''),
            'binds': bind_values}

    def add_filter(self, column, operator, value):
        self.__filters.append({
            'column': column,
            'operator': operator,
            'value': value
        })
        return self

    def page(self, page_number=0) -> list:
        """ Return [models] by page_number based on limit """
        # workaround flask-sqlalchemy/issues/516
        offset = page_number * self.limit
        sql = 'SELECT * FROM %s {} LIMIT :li OFFSET :o' \
            % (self.model.__tablename__)
        filter_query = self.__filter_query()
        if filter_query is None:
            sql = text(sql.format(''))
            result = self.model.db.engine.execute(
                sql, li=self.limit, o=offset)
        else:
            filter_query['binds']['li'] = self.limit
            filter_query['binds']['o'] = offset
            sql = text(sql.format(filter_query['query']))
            result = self.model.db.engine.execute(
                sql, **filter_query['binds'])
        result_keys = result.keys()
        result_models = []
        for row in result:
            model = self.model()
            key_count = 0
            for key in result_keys:
                setattr(model, key, row[key_count])
                key_count = key_count + 1
            result_models.append(model)
        return result_models

    def links(self, base_link, current_page) -> dict:
        """ Return JSON paginate links """
        max_pages = self.max_pages - 1 if \
            self.max_pages > 0 else self.max_pages
        base_link = '/%s' % (base_link.strip("/"))
        self_page = current_page
        prev = current_page - 1 if current_page is not 0 else None
        prev_link = '%s/page/%s/%s' % (base_link, prev, self.limit) if \
            prev is not None else None
        next = current_page + 1 if current_page < max_pages else None
        next_link = '%s/page/%s/%s' % (base_link, next, self.limit) if \
            next is not None else None
        first = 0
        last = max_pages
        return {
            'self': '%s/page/%s/%s' % (base_link, self_page, self.limit),
            'prev': prev_link,
            'next': next_link,
            'first': '%s/page/%s/%s' % (base_link, first, self.limit),
            'last': '%s/page/%s/%s' % (base_link, last, self.limit),
        }

    def json_paginate(self, base_url, page_number):
        """ Return a dict for a JSON paginate """
        data = self.page(page_number)
        first_id = None
        last_id = None
        if data:
            first_id = data[0].id
            last_id = data[-1].id
        return {
            'meta': {
                'total_pages': self.max_pages,
                'first_id': first_id,
                'last_id': last_id,
                'current_page': page_number
            },
            'data': self.page(page_number),
            'links': self.links(base_url, page_number)
        }
