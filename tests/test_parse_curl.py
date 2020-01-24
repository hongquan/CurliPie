import shlex

from devtools import debug
from curlipie.curly import CURLArgumentParser


def parsed_args(cmd_args_string):
    return CURLArgumentParser().parse_args(shlex.split(cmd_args_string))


def test_curl_form_data_single_urlencoded():
    cmline = "-d 'name=admin&shoesize=12' http://quan.hoabinh.vn"
    args = parsed_args(cmline)
    assert args.data == ['name=admin&shoesize=12']
    assert args.url == 'http://quan.hoabinh.vn'


def test_curl_form_data_multi():
    cmline = "-d name=admin -d shoesize=12 http://quan.hoabinh.vn"
    args = parsed_args(cmline)
    assert args.data == ['name=admin', 'shoesize=12']


def test_curl_form_data_multi_mixed():
    cmline = "-d name=admin -d shoesize=12 -d color=green&food=wet http://quan.hoabinh.vn"
    args = parsed_args(cmline)
    assert args.data == ['name=admin', 'shoesize=12', 'color=green&food=wet']
    debug(args._data)
    assert tuple(args._data) == (('name', 'admin'), ('shoesize', '12'),
                                 ('color', 'green'), ('food', 'wet'))


def test_head():
    cmline = "-I http://quan.hoabinh.vn"
    args = parsed_args(cmline)
    assert args.head


def test_basic_auth():
    cmline = "http://quan.hoabinh.vn --user username:password"
    args = parsed_args(cmline)
    assert args.user == 'username:password'


def test_headers():
    cmline = "--header 'Content-Type: application/json' --header 'Host: quan.hoabinh.vn' http://103.92.28.225"
    args = parsed_args(cmline)
    debug(args.header)
    assert args.header == ['Content-Type: application/json', 'Host: quan.hoabinh.vn']
    debug(args._headers)
    assert args._headers == {'Host': 'quan.hoabinh.vn'}
    assert args._request_json


def test_method():
    cmline = "--request DELETE http://quan.hoabinh.vn"
    args = parsed_args(cmline)
    assert args.request == 'DELETE'


def test_post_data():
    cmline = "-X POST http://quan.hoabinh.vn -d 'username=yourusername&password=yourpassword'"
    args = parsed_args(cmline)
    assert args.request == 'POST'
    assert args.data == ['username=yourusername&password=yourpassword']
