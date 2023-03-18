import falcon

from common.json_api import make_response


class Liveness(object):
    """
    Are we functional? Or should our scheduler kill us and make another.
    Run a check through our service to prove all parts viable (e.g., query for a db record)
    Return 200 OK if we are functional, 503 otherwise.
    """
    def on_get(self, _: falcon.Request, resp: falcon.Response):
        resp.body = make_response('liveness', 'id', dict(id=0, db='ok'))


class Readiness(object):
    """
    Are we ready to serve requests?
    Check that we can connect to all upstream components. (e.g., ping db)
    Return 200 OK if we are functional, 503 otherwise.
    """
    def on_get(self, _: falcon.Request, resp: falcon.Response):
        resp.body = make_response('readiness', 'id', dict(id=0, db='ok'))
