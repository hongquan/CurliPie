import shlex

from devtools import debug
from kiss_headers import Headers, Header
from curlipie.curly import CURLArgumentParser


def parsed_args(cmd_args_string: str) -> CURLArgumentParser:
    return CURLArgumentParser().parse_args(shlex.split(cmd_args_string))


def test_curl_form_data_single_urlencoded() -> None:
    cmline = "-d 'name=admin&shoesize=12' http://quan.hoabinh.vn"
    args = parsed_args(cmline)
    assert args.data == ['name=admin&shoesize=12']
    assert args.url == 'http://quan.hoabinh.vn'


def test_curl_form_data_multi() -> None:
    cmline = '-d name=admin -d shoesize=12 http://quan.hoabinh.vn'
    args = parsed_args(cmline)
    assert args.data == ['name=admin', 'shoesize=12']


def test_curl_form_data_multi_mixed() -> None:
    cmline = '-d name=admin -d shoesize=12 -d color=green&food=wet http://quan.hoabinh.vn'
    args = parsed_args(cmline)
    assert args.data == ['name=admin', 'shoesize=12', 'color=green&food=wet']
    debug(args._data)
    assert tuple(args._data) == (('name', 'admin'), ('shoesize', '12'), ('color', 'green'), ('food', 'wet'))


def test_head() -> None:
    cmline = '-I http://quan.hoabinh.vn'
    args = parsed_args(cmline)
    assert args.head


def test_basic_auth() -> None:
    cmline = 'http://quan.hoabinh.vn --user username:password'
    args = parsed_args(cmline)
    assert args.user == 'username:password'


def test_headers() -> None:
    cmline = "--header 'Content-Type: application/json' --header 'Host: quan.hoabinh.vn' http://103.92.28.225"
    args = parsed_args(cmline)
    debug(args.header)
    assert args.header == ['Content-Type: application/json', 'Host: quan.hoabinh.vn']
    debug(args._headers)
    assert args._headers == Headers(Header('Host', 'quan.hoabinh.vn'))
    assert args._request_json


def test_accept_json_header() -> None:
    cmline = "--header 'Accept: application/json' --header 'Host: quan.hoabinh.vn' http://103.92.28.225"
    args = parsed_args(cmline)
    assert args.header == ['Accept: application/json', 'Host: quan.hoabinh.vn']
    assert args._headers == Headers(Header('Host', 'quan.hoabinh.vn'))
    assert args._accept_json


def test_method() -> None:
    cmline = '--request DELETE http://quan.hoabinh.vn'
    args = parsed_args(cmline)
    assert args.request == 'DELETE'


def test_post_data() -> None:
    cmline = "-X POST http://quan.hoabinh.vn -d 'username=yourusername&password=yourpassword'"
    args = parsed_args(cmline)
    assert args.request == 'POST'
    assert args.data == ['username=yourusername&password=yourpassword']


def test_query_params() -> None:
    cmline = '-sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823"'
    args = parsed_args(cmline)
    assert tuple(args._params) == (('op', 'get'), ('search', '0x2EE0EA64E40A89B84B2DF73499E82A75642AC823'))


def test_upload() -> None:
    cmline = 'curl -F file=@~/path/image.png http://quan.hoabinh.vn'
    args = parsed_args(cmline)
    assert tuple(args._data) == (('file', '@~/path/image.png'),)


def test_data_raw() -> None:
    cmline = """
    --location --request POST 'https://quan.hoabinh.vn/searching?apikey=xxx'
--header 'Content-Type: application/json'
--data-raw '{
    "title": "yyy",
    "categories": [
        "zzz"
    ],
    "domain": "quan.hoabinh.vn"
}'
    """
    args = parsed_args(cmline)
    assert args.header == ['Content-Type: application/json']
    debug(args._data)
    assert tuple(args._data) == (('title', 'yyy'), ('categories', ['zzz']), ('domain', 'quan.hoabinh.vn'))
