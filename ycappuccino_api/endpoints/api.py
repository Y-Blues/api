"""
  api description for endpoint bundle
"""
from ycappuccino_api.core.api import CFQCN


class IRightManager(object):
    """ interface of service that manage right access  """
    name = CFQCN.build("IRightManager")

    def __init__(self):
        """ abstract constructor """
        pass


    def is_authorized(self, a_token, a_url_path):
        """ return true if it's authorized, else false"""
        return False


    def verify(self, a_token):
        return False




class IEndpoint(object):
    """ interface of generic endpoint that manage all redirection of request with specific parameter to a handler"""
    name = CFQCN.build("IEndpoint")

    def __init__(self):
        """ abstract constructor """

    def post(self, a_item_id, a_header, a_params, a_body):
        pass

    def put(self, a_item_id, a_header, a_params, a_body):
        pass

    def get(self, a_item_id, a_header, a_params):
        pass

    def delete(self, a_item_id, a_header, a_params):
        pass


class IHandlerEndpoint(object):
    """ interface of generic handler endpoint that manage request for specific types"""
    name = CFQCN.build("IHandlerEndpoint")

    def __init__(self):
        """ abstract constructor """

    def get_types(self):
        pass

    def post(self, a_path, a_header,  a_body):
        pass

    def put(self, a_path, a_header,  a_body):
        pass

    def get(self, a_path, a_header):
        pass

    def delete(self, a_path, a_header):
        pass
