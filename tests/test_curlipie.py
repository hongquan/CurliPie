import pytest

from devtools import debug
from curlipie.pie import curl_to_httpie


test_data = (
    ("curl -d 'name=admin&shoesize=12' http://quan.hoabinh.vn",
     "http -f http://quan.hoabinh.vn name=admin shoesize=12"),
    ("curl -d name=admin -d shoesize=12 http://quan.hoabinh.vn",
     "http -f http://quan.hoabinh.vn name=admin shoesize=12"),
    ("curl -d name=admin -d shoesize=12 -d color=green&food=wet http://quan.hoabinh.vn",
     "http -f http://quan.hoabinh.vn name=admin shoesize=12 color=green food=wet"),
    ("curl -I http://quan.hoabinh.vn",
     "http HEAD http://quan.hoabinh.vn"),
    ("curl http://quan.hoabinh.vn --user username:password",
     "http -a username:password http://quan.hoabinh.vn"),
    ("curl --header 'Content-Type: application/json' --header 'Host: quan.hoabinh.vn' http://103.92.28.225",
     "http http://103.92.28.225 Host:quan.hoabinh.vn Content-Type:application/json"),
    ("curl --request DELETE http://quan.hoabinh.vn",
     "http DELETE http://quan.hoabinh.vn"),
    ("curl -X POST http://quan.hoabinh.vn -d 'username=yourusername&password=yourpassword'",
     "http -f http://quan.hoabinh.vn username=yourusername password=yourpassword"),
)


@pytest.mark.parametrize('curl, expected', test_data)
def test_converting(curl, expected):
    httpie = curl_to_httpie(curl)
    assert httpie == expected


def test_json_form():
    curl = ("""curl -XPUT elastic.dev/movies/_doc/1 -d '{"director": "Burton, Tim", """
            """ "year": 1996, "title": "Mars Attacks!"}' -H 'Content-Type: application/json'""")
    output = curl_to_httpie(curl)
    assert output == ("""http PUT elastic.dev/movies/_doc/1 director='Burton, Tim' """
                      """year:=1996 title='Mars Attacks!'""")


def test_json_value_not_primitive():
    curl = ("""curl -XPUT elastic.dev/movies/_doc/1 -d '{"genre": ["Comedy", "Sci-Fi"],"""
            """ "actor": ["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"]}' """
            """-H 'Content-Type: application/json'""")
    output = curl_to_httpie(curl)
    debug(output)
    assert output == ("""http PUT elastic.dev/movies/_doc/1 genre:='["Comedy","Sci-Fi"]' """
                      """actor:='["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"]'""")
