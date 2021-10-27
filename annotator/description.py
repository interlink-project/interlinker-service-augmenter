from annotator import es,authz

TYPE = 'description'
MAPPING = {

    "id": {
        "type": "string",
        "index": "no"
    },

    "title": {
        "type": "string",
        "analyzer": "standard"
    },

    "description": {
        "type": "string",
        "analyzer": "standard"
    },

    "keywords": {
        "type": "string",
        "analyzer": "standard"
    },

    "moderators": {
        "type": "string",
        "analyzer": "standard"
    },

    'moderators': {
        'type': 'nested',
        'properties': {
            'email': {'type': 'string'},
            'created': {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
            'expire': {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
        }
    },

    "padministration": {
        "type": "string",
        "analyzer": "standard"
    },

    "url": {
        "type": "string",
        "analyzer": "standard"
    },

    "created": {
        "type": "date",
        "format": "dateOptionalTime"
    },

    "updated": {
        "type": "date",
        "format": "dateOptionalTime"
    },


}
MAX_ITERATIONS = 5


class Description(es.Model):
    __type__ = TYPE
    __mapping__ = MAPPING

   
    __type__ = TYPE
    __mapping__ = MAPPING

    def save(self, *args, **kwargs):
        _add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        

        super(Description, self).save(*args, **kwargs)

    @classmethod
    def search_raw(cls, query=None, params=None, raw_result=False,
                   user=None, authorization_enabled=None):
        """Perform a raw Elasticsearch query

        Any ElasticsearchExceptions are to be caught by the caller.

        Keyword arguments:
        query -- Query to send to Elasticsearch
        params -- Extra keyword arguments to pass to Elasticsearch.search
        raw_result -- Return Elasticsearch's response as is
        user -- The user to filter the results for according to permissions
        authorization_enabled -- Overrides Description.es.authorization_enabled
        """
        if query is None:
            query = {}
        if authorization_enabled is None:
            authorization_enabled = es.authorization_enabled
        if authorization_enabled:
            f = authz.permissions_filter(user)
            if not f:
                raise RuntimeError("Authorization filter creation failed")
            filtered_query = {
                'filtered': {
                    'filter': f
                }
            }
            # Insert original query (if present)
            if 'query' in query:
                filtered_query['filtered']['query'] = query['query']
            # Use the filtered query instead of the original
            query['query'] = filtered_query

        res = super(Description, cls).search_raw(query=query, params=params,
                                                raw_result=raw_result)
        return res

    @classmethod
    def _build_query(cls, query=None, offset=None, limit=None, sort=None, order=None):
        if query is None:
            query = {}
        else:
            query = dict(query)  # shallow copy

        # Pop 'before' and 'after' parameters out of the query
        after = query.pop('after', None)
        before = query.pop('before', None)

        q = super(Description, cls)._build_query(query, offset, limit, sort, order)

        # Create range query from before and/or after
        if before is not None or after is not None:
            clauses = q['query']['bool']['must']

            # Remove match_all conjunction, because
            # a range clause is added
            if clauses[0] == {'match_all': {}}:
                clauses.pop(0)

            created_range = {'range': {'created': {}}}
            if after is not None:
                created_range['range']['created']['gte'] = after
            if before is not None:
                created_range['range']['created']['lt'] = before
            clauses.append(created_range)

        

        return q


def _add_default_permissions(ann):
    if 'permissions' not in ann:
        ann['permissions'] = {'read': [authz.GROUP_CONSUMER]}
