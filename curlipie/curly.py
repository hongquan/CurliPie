
from itertools import chain
from typing import List, Tuple, Optional
from collections import OrderedDict
from urllib.parse import parse_qsl, urlsplit, SplitResult

import hh
from tap import Tap

from .structures import CaseInsensitiveDict


# Ref: https://helpmanual.io/help/curl/
class CURLArgumentParser(Tap):
    url: str
    verbose: bool = False
    include: bool = False
    request: Optional[str] = None
    user: Optional[str] = None
    header: List[str] = []
    form: List[str] = []
    data: List[str] = []
    head: bool = False
    output: Optional[str] = None
    http2: bool = False
    # Intermediate converted data
    _url: str = None
    _params: List[Tuple[str, str]] = []
    _data: List[Tuple[str, str]] = []
    _headers: CaseInsensitiveDict = None
    _request_json: bool = False

    def _get_class_variables(self) -> OrderedDict:
        '''Overide to exclude our private variables'''
        all_variables = super()._get_class_variables()
        return OrderedDict((k, v) for k, v in all_variables.items() if not k.startswith('_'))

    def add_arguments(self):
        self.add_argument('url')
        self.add_argument('-v', '--verbose')
        self.add_argument('-i', '--include')
        self.add_argument('-X', '--request')
        self.add_argument('-u', '--user')
        self.add_argument('-H', '--header', nargs='?', action='append')
        self.add_argument('-d', '--data', nargs='?', action='append')
        self.add_argument('-F', '--form')
        self.add_argument('-I', '--head')
        self.add_argument('-o', '--output')
        self._headers = CaseInsensitiveDict()

    def process_args(self):
        u = urlsplit(self.url)    # type: SplitResult
        self._url = f'{u.scheme}://{u.netloc}{u.path}'
        self._params = parse_qsl(u.query)
        self._data = list(chain.from_iterable(parse_qsl(d) for d in self.data))
        for h in self.header:
            k, v = h.split(':')
            k = k.strip()     # type: str
            v = v.strip()     # type: str
            if k.lower() == hh.CONTENT_TYPE.lower() and v.lower().endswith('/json'):
                self._request_json = True
                continue
            self._headers[k] = v

    def error(self, message):
        # Override to not let it exit our program
        pass
