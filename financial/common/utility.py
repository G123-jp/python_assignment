import datetime
import json
from uuid import uuid4

import falcon


class DictMixin(object):

    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, DictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)


def falcon_error_serializer(_: falcon.Request,
                            resp: falcon.Response,
                            exc: falcon.HTTPError) -> None:
    """ Serializer for native falcon HTTPError exceptions.

    Serializes HTTPError classes as proper json:api error
        see: http://jsonapi.org/format/#errors
    """
    error = {
        'id': str(uuid4()),
        'title': exc.title,
        'detail': exc.description,
        'status': exc.status[0:3],
    }

    if hasattr(exc, "link") and exc.link is not None:
        error['links'] = {'about': exc.link['href']}

    resp.body = json.dumps({'errors': [error]})


def current_utc_timestamp():
    """
    Return current UTC timestamp
    """
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()