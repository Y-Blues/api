import json
import unittest
import warnings

import ycappuccino.api.endpoints as endpoints
from ycappuccino.api.endpoints import (
    EndpointResponse,
    EndpointResponseModel,
    UrlPath,
    get_token_from_header,
)


class FakeApiDescription(object):
    def __init__(self, paths):
        self._body = {"paths": {path: {} for path in paths}}


API_DESCRIPTION = FakeApiDescription(
    ["/$endpoint_crud/books", "/$endpoint_crud/books/{id}", "/$service/login"]
)


class TestTokenFromHeader(unittest.TestCase):

    def test_bearer_authorization(self):
        self.assertEqual(get_token_from_header({"authorization": "Bearer abc"}), "abc")

    def test_authorization_without_bearer(self):
        self.assertIsNone(get_token_from_header({"authorization": "Basic abc"}))

    def test_ycappuccino_cookie_among_others(self):
        headers = {"Cookie": "lang=fr; _ycappuccino=abc; theme=dark"}

        self.assertEqual(get_token_from_header(headers), "abc")

    def test_single_ycappuccino_cookie(self):
        self.assertEqual(get_token_from_header({"Cookie": "_ycappuccino=abc"}), "abc")

    def test_cookies_without_ycappuccino_token(self):
        for cookie in ("lang=fr; theme=dark", "lang=fr", "garbage"):
            with self.subTest(cookie=cookie):
                self.assertIsNone(get_token_from_header({"Cookie": cookie}))

    def test_no_credentials(self):
        self.assertIsNone(get_token_from_header({}))


class TestEndpointResponse(unittest.TestCase):

    def test_body_only_when_no_meta(self):
        self.assertEqual(json.loads(EndpointResponse(200, a_body={"a": 1}).get_json()), {"a": 1})

    def test_empty_array_response(self):
        response = EndpointResponse(200, a_meta={"type": "array"})

        self.assertEqual(json.loads(response.get_json())["data"], [])

    def test_model_response_unwraps_a_single_model(self):
        response = EndpointResponseModel(
            200, a_meta={"type": "object"}, a_body={"_mongo_model": {"title": "x"}}
        )

        self.assertEqual(json.loads(response.get_json())["data"], {"title": "x"})

    def test_model_response_unwraps_a_list_of_models(self):
        response = EndpointResponseModel(
            200,
            a_meta={"type": "array"},
            a_body=[{"_mongo_model": {"title": "x"}}, {"_mongo_model": {"title": "y"}}],
        )

        self.assertEqual(json.loads(response.get_json())["data"], [{"title": "x"}, {"title": "y"}])

    def test_model_response_keeps_a_list_of_plain_dicts(self):
        response = EndpointResponseModel(200, a_meta={"type": "array"}, a_body=[{"title": "x"}])

        self.assertEqual(json.loads(response.get_json())["data"], [{"title": "x"}])


class TestUrlPath(unittest.TestCase):

    def test_crud_url_with_path_and_query_parameters(self):
        url = UrlPath("get", "/api/$endpoint_crud/books/12?draft=1", API_DESCRIPTION)

        self.assertEqual(url.get_type(), "endpoint_crud")
        self.assertFalse(url.is_service())
        self.assertEqual(url.get_params(), {"draft": "1", "id": "12"})

    def test_service_url(self):
        url = UrlPath("post", "/api/$service/login", API_DESCRIPTION)

        self.assertTrue(url.is_service())
        self.assertEqual(url.get_service_name(), "login")

    def test_module_has_no_invalid_escape_sequences(self):
        with open(endpoints.__file__) as source:
            content = source.read()

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            compile(content, endpoints.__file__, "exec")


if __name__ == "__main__":
    unittest.main()
