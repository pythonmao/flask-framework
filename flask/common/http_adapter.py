import json
import requests
import logging
from oslo_log import log
from bmc.common.exception import XClarityConnectionFailed, XClarityInternalFault

LOG = log.getLogger(__name__)


class HttpMethod:
    def do_get_request(self, url, headers=None, body=None, auth=None, verify=False):
        status_code, text = self.__do_http_request("GET", url, headers, body, auth, verify)
        try:
            return json.loads(text)
        except (TypeError, ValueError):
            LOG.error("can not parse http response text to json", text)
            return None

    def do_post_request(self, url, headers=None, body=None, auth=None, verify=False):
        try:
            self.__do_http_request("POST", url, headers, body, auth, verify)
            return True
        except Exception as ex:
            LOG.error("send post http request raise an Exception \n %s" % ex)
            return False

    # --------------------- helper functions -------------------- #

    def __do_http_request(self, method, url, headers=None, body=None, auth=None, verify=False):
        try:
            self.__http_log_req(method, url, body, headers)
            resp = requests.request(method,
                                    url,
                                    data=body,
                                    headers=headers,
                                    auth=auth,
                                    verify=verify)
            self.__http_log_resp(resp, resp.text)
            status_code = resp.status_code
            return status_code, resp.text if status_code < 300 else self.__handle_fault_response(resp)
        except requests.exceptions.ConnectionError as e:
            LOG.debug("throwing ConnectionFailed : %s", e)
            raise XClarityConnectionFailed(explanation='Http ConnectionFailed')

    def __handle_fault_response(self, resp):
        LOG.debug("Error message: %s", resp.text)
        try:
            error_body = json.loads(resp.text)
            if error_body:
                explanation = error_body['messages'][0]['explanation']
                recovery = error_body['messages'][0]['recovery']['text']
        except Exception:
            # If unable to deserialized body it is probably not a
            explanation = resp.text
            recovery = ''
        # Raise the appropriate exception
        kwargs = {'explanation': explanation, 'recovery': recovery}
        raise XClarityInternalFault(**kwargs)

    def __http_log_req(self, method, url, body=None, headers=None):
        if not LOG.isEnabledFor(logging.DEBUG):
            return
        LOG.debug("REQ:%(method)s %(url)s %(headers)s %(body)s\n",
                       {'method': method,
                        'url': url,
                        'headers': headers,
                        'body': body})

    def __http_log_resp(self, resp, body):
        if not LOG.isEnabledFor(logging.DEBUG):
            return
        LOG.debug("RESP:%(code)s %(headers)s %(body)s\n",
                       {'code': resp.status_code,
                        'headers': resp.headers,
                        'body': body})


