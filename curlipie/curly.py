
import collections.abc
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict, deque
from urllib.parse import parse_qsl

import yarl
from tap import Tap
from logbook import Logger
from kiss_headers import parse_it, get_polymorphic, ContentType, BasicAuthorization
from kiss_headers import Headers, Header
from http_constants.headers import HttpHeaders as HH

from .compat import json_load, JSONDecodeError


logger = Logger(__name__)


@dataclass
class DataArgParseResult:
    data: List[Tuple[str, str]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# Ref: https://helpmanual.io/help/curl/
class CURLArgumentParser(Tap):
    url: str
    verbose: bool = False
    include: bool = False
    location: bool = False
    append: bool = False
    silent: bool = False
    fail: bool = False
    show_error: bool = False
    globoff: bool = False
    insecure: bool = False
    http1_0: bool = False
    tlsv1: bool = False
    sslv2: bool = False
    sslv3: bool = False
    netrc: bool = False
    proxytunnel: bool = False
    use_ascii: bool = False
    no_buffer: bool = False
    remote_name: bool = False
    remote_time: bool = False
    remote_header_name: bool = False
    max_redirs: int = 0
    max_time: float = 0
    request: Optional[str] = None
    proxy: Optional[str] = None
    user: Optional[str] = None
    cert: Optional[str] = None
    cacert: Optional[str] = None
    header: List[str] = []
    form: List[str] = []
    data: List[str] = []
    data_raw: List[str] = []
    data_binary: List[str] = []
    user_agent: Optional[str] = None
    head: bool = False
    get: bool = False
    output: Optional[str] = None
    http2: bool = False
    # Intermediate converted data
    _url: str = ''
    _auth: Optional[BasicAuthorization] = None
    _params: List[Tuple[str, str]] = []
    _data: List[Tuple[str, str]] = []
    _headers: Headers
    _request_json: bool = False
    _errors: List[str] = []

    def _get_class_variables(self) -> OrderedDict:
        '''Overide to exclude our private variables'''
        all_variables = super()._get_class_variables()
        return OrderedDict((k, v) for k, v in all_variables.items() if not k.startswith('_'))

    def configure(self):
        self.add_argument('url')
        self.add_argument('-v', '--verbose')
        self.add_argument('-i', '--include')
        self.add_argument('-L', '--location')
        self.add_argument('-a', '--append')
        self.add_argument('-s', '--silent')
        self.add_argument('-f', '--fail')
        self.add_argument('-S', '--show-error')
        self.add_argument('-g', '--globoff')
        self.add_argument('-k', '--insecure')
        self.add_argument('-0', '--http1.0', dest='http1_0')
        self.add_argument('-1', '--tlsv1')
        self.add_argument('-2', '--sslv2')
        self.add_argument('-3', '--sslv3')
        self.add_argument('-n', '--netrc')
        self.add_argument('-p', '--proxytunnel')
        self.add_argument('-B', '--use-ascii')
        self.add_argument('-N', '--no-buffer')
        self.add_argument('-O', '--remote-name')
        self.add_argument('-R', '--remote-time')
        self.add_argument('-J', '--remote-header-name')
        self.add_argument('-X', '--request')
        self.add_argument('-m', '--max-time')
        self.add_argument('-x', '--proxy', nargs='?')
        self.add_argument('-u', '--user')
        self.add_argument('-E', '--cert')
        self.add_argument('--cacert')
        self.add_argument('-H', '--header', nargs='?', action='append')
        self.add_argument('-d', '--data', nargs='?', action='append')
        self.add_argument('--data-raw', nargs='?', action='append', default=[])
        self.add_argument('--data-binary', nargs='?', action='append')
        self.add_argument('-F', '--form', nargs='?', action='append')
        self.add_argument('-A', '--user-agent')
        self.add_argument('-I', '--head')
        self.add_argument('-G', '--get')
        self.add_argument('-o', '--output')
        self._headers = Headers()

    def process_args(self):
        u = yarl.URL(self.url)
        # Clean fragment, if exist
        url = str(u.with_fragment(None).with_query(None))
        # Strip leading "http://" to be short
        self._url = url[7:] if u.scheme == 'http' else url
        self._params = deque(u.query.items())
        self._data = deque()
        for dstring in self.data:
            result = parse_post_data(dstring)
            self._data.extend(result.data)
            self._errors.extend(result.errors)
        for dstring in self.data_raw:
            result = parse_post_data(dstring, ignore_at=True)
            self._data.extend(result.data)
            self._errors.extend(result.errors)
        for dstring in self.form:
            result = parse_post_data(dstring)
            self._data.extend(result.data)
            self._errors.extend(result.errors)
        for h in self.header:
            headers = parse_it(h)
            if not headers:
                continue
            if HH.CONTENT_TYPE in headers:
                hx = get_polymorphic(headers, ContentType)
                if hx.get_mime() == HH.CONTENT_TYPE_VALUES.json:
                    self._request_json = True
                    continue
            elif HH.AUTHORIZATION in headers and headers.authorization.content.startswith('Basic '):
                hx = get_polymorphic(headers, BasicAuthorization)
                self._auth = hx
                continue
            # kiss-header doesn't prevent duplicate, so we have to check ourselve
            # Please note the behavior of kiss-headers: The "Accept-Encoding: gzip, deflate"
            # will be parsed to two Header objects, to get all the "value" side, we have to
            # convert the parse result to dict.
            name = headers[0].pretty_name
            if self._headers.has(name):
                del self._headers[name]
            value = headers.to_dict()[name]
            self._headers += Header(name, value)

    def error(self, message):
        # Override to prevent parser from terminating our program
        pass


def parse_post_data(string: str, ignore_at: bool = False) -> DataArgParseResult:
    # https://ec.haxx.se/http/http-post
    if not string:
        return DataArgParseResult()
    data = parse_qsl(string)
    if data:
        return DataArgParseResult(data=data)
    # Standard parse_qsl failed to parse it
    if not ignore_at and '@' in string and not string.startswith('@'):
        # cURL spec says that the filename should already be url-encoded.
        key, filename = string.split('@')[:2]
        return DataArgParseResult(data=[(key, filename)])
    # HTTPie doesn't support sending raw content as request body
    # (though it allows to specify raw content as the value for a field),
    # so we can ignore cURL "content", "=content", "@filename" syntaxes.
    errors = deque()
    if string.startswith('@'):
        errors.append('@filename syntax (without field name) is not supported')
        return DataArgParseResult(data, errors)
    if string.startswith('='):
        errors.append('=content syntax (without field name) is not supported')
        return DataArgParseResult(data, errors)
    # Maybe JSON?
    try:
        jsdata = json_load(string)
    except JSONDecodeError:
        # Not JSON
        errors.append('Cannot guess post data format')
        return DataArgParseResult(data, errors)
    if isinstance(jsdata, collections.abc.Mapping):
        data = list(jsdata.items())
        return DataArgParseResult(data, errors)
    errors.append('JSON content does not represent an object')
    return DataArgParseResult(errors=errors)
