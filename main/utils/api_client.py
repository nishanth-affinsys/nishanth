import json as j
import logging
import requests
from django.conf import settings

LOGGER_NAME = getattr(settings, "DJANGO_APICLIENT_LOGGING_LOGGER_NAME", "django.api")

logger = logging.getLogger(LOGGER_NAME)


class APIClient:
    def log_request(self, method, url, params, headers, files, data, json_data):
        if headers is not None:
            headers = self.mask(headers, settings.REQUEST_LOGGING_SENSITIVE_HEADERS)
        if data is not None:
            if type(data) == list:
                data = [
                    self.mask(d, settings.REQUEST_LOGGING_SENSITIVE_POST_PARAMS)
                    for d in data
                ]
            else:
                data = self.mask(data, settings.REQUEST_LOGGING_SENSITIVE_POST_PARAMS)

        if json_data is not None:
            if type(json_data) == list:
                json_data = [
                    self.mask(d, settings.REQUEST_LOGGING_SENSITIVE_POST_PARAMS)
                    for d in json_data
                ]
            else:
                json_data = self.mask(
                    json_data, settings.REQUEST_LOGGING_SENSITIVE_POST_PARAMS
                )

        data_dict = {"data": data, "files": files, "json": json_data}

        logger.info(
            f"Request for url {method}:{url} with data {data_dict} with params {params} and headers {headers}"
        )

    def log_response(self, response_data: requests.Response):
        status_code = response_data.status_code
        headers = response_data.request.headers
        data = response_data.content
        if data != b"":
            data = j.loads(data)
            if type(data) == list:
                data = [
                    self.mask(d, settings.RESPONSE_LOGGING_SENSITIVE_BODY_PARAMS)
                    for d in data
                ]
            else:
                data = self.mask(data, settings.RESPONSE_LOGGING_SENSITIVE_BODY_PARAMS)
        url = response_data.request.url
        method = response_data.request.method
        headers = self.mask(headers, settings.RESPONSE_LOGGING_SENSITIVE_HEADERS)
        logger.info(
            f"Response for {method}: {url} with headers {headers} is {status_code}: {data}"
        )

    def mask(self, dict_to_mask, masks):
        masked_dict = {}
        for key in dict_to_mask:
            if type(dict_to_mask[key]) == dict:
                masked_dict[key] = self.mask(dict_to_mask[key], masks)
                continue
            if key in masks:
                masked_dict[key] = "*****"
            else:
                masked_dict[key] = dict_to_mask[key]
        return masked_dict

    def get(self, url, params=None, headers=None, timeout=None):
        return self.call_external_api(
            method="get", url=url, params=params, headers=headers, timeout=timeout
        )

    def post(
        self,
        url,
        params=None,
        headers=None,
        timeout=None,
        data=None,
        json=None,
        files=None,
    ):
        return self.call_external_api(
            method="post",
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            json=json,
            files=files,
        )

    def put(
        self,
        url,
        params=None,
        headers=None,
        timeout=None,
        data=None,
        json=None,
        files=None,
    ):
        return self.call_external_api(
            method="put",
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            json=json,
            files=files,
        )

    def patch(
        self,
        url,
        params=None,
        headers=None,
        timeout=None,
        data=None,
        json=None,
        files=None,
    ):
        return self.call_external_api(
            method="patch",
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            json=json,
            files=files,
        )

    def delete(
        self,
        url,
        params=None,
        headers=None,
        timeout=None,
        data=None,
        json=None,
        files=None,
    ):
        return self.call_external_api(
            method="delete",
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            json=json,
            files=files,
        )

    def call_external_api(
        self,
        method,
        url,
        headers: dict = None,
        params=None,
        data=None,
        json=None,
        files=None,
        timeout=settings.DEFAULT_REQUEST_TIMEOUT,
    ):
        try:
            self.log_request(
                url=url,
                params=params,
                headers=headers,
                method=method,
                data=data,
                json_data=json,
                files=files,
            )
            response = requests.request(
                method.lower(),
                url,
                params=params,
                headers=headers,
                data=data,
                json=json,
                files=files,
                timeout=timeout,
            )
            response_json = {} if response.text == "" else response.json()
            self.log_response(response_data=response)
            return response_json, response.status_code, response.headers

        except AssertionError:
            raise AssertionError("Incorrect method passed!")

        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout(
                "Connection to the remote server timed out"
            )

        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError(
                "Could not connect to the remote server"
            )

        except requests.exceptions.InvalidURL:
            raise requests.exceptions.InvalidURL("Could not parse URL")

        except requests.exceptions.InvalidHeader as ihe:
            raise requests.exceptions.InvalidHeader(
                f"Could not parse Headers provided:{ihe}"
            )

        except requests.exceptions.JSONDecodeError as e:
            raise requests.exceptions.JSONDecodeError(
                f"Response from {url} is text and not JSON-able", e.doc, e.pos
            )

        except requests.exceptions.RequestException as re:
            raise requests.exceptions.RequestException(
                f"Request unexpectedly failed: {re}"
            )

        except Exception as e:
            raise Exception(f"Error in fetching request: {e}")
