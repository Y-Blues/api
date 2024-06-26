"""
  api description for endpoint bundle
"""

from ycappuccino.api.proxy import CFQCN
from ycappuccino.api.proxy import YCappuccinoRemote


import logging

"""
   utilities to read header
"""

_logger = logging.getLogger(__name__)


"""
    bean that provide request and response object
"""

import json, re
from urllib.parse import parse_qsl, urlsplit


class EndpointResponse(object):

    def __init__(self, status, a_header=None, a_meta=None, a_body=None):
        """need status"""
        self._status = status
        self._meta = a_meta
        self._header = a_header
        self._body = a_body

    def get_header(self):
        return self._header

    def get_json(self):
        if self._meta is None:
            return json.dumps(self._body)
        else:
            w_resp = {"status": self._status, "meta": self._meta, "data": None}
            if self._body is not None:
                if isinstance(self._body, dict):
                    w_resp["data"] = self._body
                elif isinstance(self._body, list):
                    w_body = []
                    if len(self._body) > 0:
                        for w_json in self._body:
                            w_body.append(w_json)
                    w_resp["data"] = w_body
            else:
                if w_resp["meta"]["type"] == "array":
                    w_resp["data"] = []
                else:
                    w_resp["data"] = {}

            return json.dumps(w_resp)

    def get_status(self):
        return self._status


class UrlPath(object):

    def __init__(self, a_method, a_url, a_api_description):
        """need status"""
        self._url = a_url
        w_url_no_query = a_url
        w_url_query = a_url
        self._method = a_method
        self._query_param = None
        if "?" in a_url:
            self._query_param = dict(parse_qsl(urlsplit(a_url).query))
            w_url_no_query = w_url_no_query.split("?")[0]
            w_url_query = w_url_query.split("?")[1]

        self._split_url = w_url_no_query.split("api/")[1].split("/")
        self._type = self._split_url[0][1:]
        self._is_service = "$service" in self._split_url

        if self._is_service:
            self._service_name = self._split_url[1]
        self._url_no_query = w_url_no_query.split("api/")[1]
        self._url_param = w_url_query
        if len(self.get_split_url()) > 1:
            self._item_plural_id = self.get_split_url()[1]
        # retrieve description url
        for w_path in a_api_description._body["paths"].keys():
            w_path_pattern = (
                re.sub("\{.*\}", ".*", w_path).replace("/", "\/").replace("$", "\$")
                + "$"
            )
            if re.search(w_path_pattern, "/" + self._url_no_query):
                w_path_split = w_path[1:].split("/")
                i = 0
                for w_part in w_path_split:
                    if w_part[0] == "{" and w_part[-1] == "}":
                        if self._query_param is None:
                            self._query_param = {}
                        self._query_param[w_part[1:-1]] = self.get_split_url()[i]
                    i = i + 1

    def get_split_url(self):
        return self._split_url

    def get_url_no_query(self):
        return self._url_no_query

    def get_url_query(self):
        return self._url_param

    def get_method(self):
        return self._method

    def get_type(self):
        return self._type

    def is_service(self):
        return self._is_service

    def get_service_name(self):
        return self._service_name

    def get_params(self):
        return self._query_param


class EndpointResponseModel(EndpointResponse):

    def __init__(
        self,
        status,
        a_header=None,
        a_meta=None,
        a_body=None,
        a_storage_property="_mongo_model",
    ):
        """need status"""
        super(EndpointResponseModel, self).__init__(status, a_header, a_meta, a_body)
        self._storage_property = a_storage_property

    def get_json(self):
        if self._meta is None:
            return json.dumps(self._body)
        else:
            w_resp = {"status": self._status, "meta": self._meta, "data": None}
            if self._body is not None:
                if isinstance(self._body, dict):
                    w_resp["data"] = self._body
                if self._storage_property in self._body.keys():
                    w_resp["data"] = self._body[self._storage_property]
                elif isinstance(self._body, list):
                    w_body = []
                    if len(self._body) > 0:
                        if self._storage_property in self._body[0].keys():
                            for w_model in self._body:
                                w_body.append(w_model[self._storage_property])
                        else:
                            for w_json in self._body:
                                w_body.append(w_json)
                    w_resp["data"] = w_body
            else:
                if w_resp["meta"]["type"] == "array":
                    w_resp["data"] = []
                else:
                    w_resp["data"] = {}

            return json.dumps(w_resp)


class UrlPathModel(UrlPath):

    def __init__(self, a_method, a_url, a_api_description):
        """need status"""
        super().__init__(a_method, a_url, a_api_description)

        self._is_schema = "$schema" in self.get_split_url()
        self._is_multipart = "$multipart" in self.get_split_url()

        self._is_empty = "$empty" in self.get_split_url()

    def is_crud(self):
        return not self._is_schema and not self._is_empty and not self._is_multipart

    def is_draft(self):
        return self._query_param is not None and "draft" in self._query_param

    def get_draft(self):
        return self._query_param["draft"] if self.is_draft() else None

    def is_schema(self):
        return self._is_schema

    def is_multipart(self):
        return self._is_multipart

    def is_empty(self):
        return self._is_empty

    def get_item_plural_id(self):
        return self._item_plural_id


def check_header(a_jwt, a_headers):
    w_token = get_token_from_header(a_headers)
    if w_token is None:
        return False
    return a_jwt.verify(w_token)


def get_token_decoded(a_jwt, a_headers):
    w_token = get_token_from_header(a_headers)
    if w_token is None:
        return False
    return a_jwt.get_token_decoded(w_token)


def get_token_from_header(a_headers):
    if "authorization" in a_headers:
        w_authorization = a_headers["authorization"]
        if w_authorization is not None and "Bearer" in w_authorization:
            w_token = w_authorization[len("Bearer ") :]
            return w_token
        else:
            return None
    elif "Cookie" in a_headers:
        w_cookies = a_headers["Cookie"]
        w_token = ""
        if ";" in w_cookies:
            w_arr = w_cookies.split(";")
            for w_cookie in w_arr:
                if "_ycappuccino" in w_cookie:
                    w_token = w_cookie.split("=")[1]
        else:
            w_token = w_cookies.split("=")[1]
        _logger.info("token {}".format(w_token))
        return w_token


class IRightManager(YCappuccinoRemote):
    """interface of service that manage right access"""

    name = CFQCN.build("IRightManager")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

    def is_authorized(self, a_token, a_url_path):
        """return true if it's authorized, else false"""
        return False

    def verify(self, a_token):
        return False

    def get_tokens_decoded(self):
        return None

    def get_token_decoded(self, a_token):

        return None


class IEndpoint(YCappuccinoRemote):
    """interface of generic endpoint that manage all redirection of request with specific parameter to a handler"""

    name = CFQCN.build("IEndpoint")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

    def post(self, a_item_id, a_header, a_params, a_body):
        pass

    def put(self, a_item_id, a_header, a_params, a_body):
        pass

    def get(self, a_item_id, a_header, a_params):
        pass

    def delete(self, a_item_id, a_header, a_params):
        pass


class IHandlerEndpoint(YCappuccinoRemote):
    """interface of generic handler endpoint that manage request for specific types"""

    name = CFQCN.build("IHandlerEndpoint")

    def __init__(self):
        """abstract constructor"""
        super(YCappuccinoRemote, self).__init__()

    def get_types(self):
        pass

    def post(self, a_path, a_header, a_body):
        pass

    def put(self, a_path, a_header, a_body):
        pass

    def get(self, a_path, a_header):
        pass

    def delete(self, a_path, a_header):
        pass
