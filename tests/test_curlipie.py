import pytest

from devtools import debug
from curlipie.pie import curl_to_httpie


test_data = (
    ("curl -d 'name=admin&shoesize=12' http://quan.hoabinh.vn",
     "http -f quan.hoabinh.vn name=admin shoesize=12"),
    ("curl -d name=admin -d shoesize=12 https://quan.hoabinh.vn",
     "http -f https://quan.hoabinh.vn name=admin shoesize=12"),
    ("curl -d name=admin -d shoesize=12 -d color=green&food=wet quan.hoabinh.vn",
     "http -f quan.hoabinh.vn name=admin shoesize=12 color=green food=wet"),
    ("curl -I http://quan.hoabinh.vn",
     "http HEAD quan.hoabinh.vn"),
    ("curl http://quan.hoabinh.vn --user username:password",
     "http -a username:password quan.hoabinh.vn"),
    ("curl --header 'Content-Type: application/json' --header 'Host: quan.hoabinh.vn' http://103.92.28.225",
     "http 103.92.28.225 Host:quan.hoabinh.vn Content-Type:application/json"),
    ("curl --request DELETE http://quan.hoabinh.vn/users/1",
     "http DELETE quan.hoabinh.vn/users/1"),
    ("curl -X POST http://quan.hoabinh.vn -d 'username=yourusername&password=yourpassword'",
     "http -f quan.hoabinh.vn username=yourusername password=yourpassword"),
    ("curl -X POST http://quan.hoabinh.vn/api/users --user admin:xxx -d name=meow",
     "http -fa admin:xxx quan.hoabinh.vn/api/users name=meow")
)


@pytest.mark.parametrize('curl, expected', test_data)
def test_converting(curl, expected):
    httpie = curl_to_httpie(curl).httpie
    assert httpie == expected


def test_json_form():
    curl = ("""curl -XPUT elastic.dev/movies/_doc/1 -d '{"director": "Burton, Tim", """
            """ "year": 1996, "title": "Mars Attacks!"}' -H 'Content-Type: application/json'""")
    output = curl_to_httpie(curl).httpie
    assert output == ("""http PUT elastic.dev/movies/_doc/1 director='Burton, Tim' """
                      """year:=1996 title='Mars Attacks!'""")


def test_json_value_not_primitive():
    curl = ("""curl -XPUT elastic.dev/movies/_doc/1 -d '{"genre": ["Comedy", "Sci-Fi"],"""
            """ "actor": ["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"]}' """
            """-H 'Content-Type: application/json'""")
    output = curl_to_httpie(curl).httpie
    debug(output)
    assert output == ("""http PUT elastic.dev/movies/_doc/1 genre:='["Comedy","Sci-Fi"]' """
                      """actor:='["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"]'""")


def test_curl_postman_generated():
    curl = ("""curl --location --request POST 'http://stupid.site/sync-info' \\"""
            """--header 'Content-Type: application/json' \\"""
            "--data-raw '{"
            '    "userId": "4-abc-xyz",'
            '    "planAmount": 50000,'
            '    "isPromotion": false,'
            '    "createdAt": "2019-12-13 10:00:00"'
            "}'")
    httpie = curl_to_httpie(curl).httpie
    assert httpie == ("""http -F stupid.site/sync-info userId=4-abc-xyz planAmount:=50000 """
                      """isPromotion:=false createdAt='2019-12-13 10:00:00'""")
