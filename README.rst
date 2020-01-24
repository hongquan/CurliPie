========
CurliPie
========

.. image:: https://madewithlove.now.sh/vn?heart=true&colorA=%23ffcd00&colorB=%23da251d
.. image:: https://badgen.net/pypi/v/curlipie

Python library to convert `cURL`_ command to `HTTPie`_.

It will convert

.. code-block:: sh

    curl -d name=admin -d shoesize=12 -d color=green&food=wet http://quan.hoabinh.vn

to

.. code-block:: sh

    http -f http://quan.hoabinh.vn name=admin shoesize=12 color=green food=wet


Motivation
----------

This library was born when I join a project with a team of non-Linux, non-Python developers. Because the project doesn't have proper documentation, the other team often share API usage example to me in form of cURL command, generated from their daily-used Postman. Those cURL commands are usually ugly, like this:


.. code-block:: sh

    curl --location --request POST 'http://app-staging.dev/api' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "userId": "abc-xyz",
        "planAmount": 50000,
        "isPromotion": false,
        "createdAt": "2019-12-13 10:00:00"
    }'

I am more comfortable with HTTPie (shorter syntax, has highlighting and is a Python application), so I often convert it to HTTPie:

.. code-block:: sh

    http -F app-staging.dev/api userId=abc-xyz planAmount:=50000 isPromotion:=false createdAt='2019-12-13 10:00:00'

The Postman tool can generate HTTPie, but with even uglier command:

.. code-block:: sh

    printf '{
        "userId": "abc-xyz",
        "planAmount": 50000,
        "isPromotion": false,
        "createdAt": "2019-12-13 10:00:00"
    }'| http  --follow --timeout 3600 POST app-staging.dev/api \
    Content-Type:'application/json'

Initially, I had to do conversion manually and quickly got tired from it. I tried to find a conversion tool but failed. There is an online tool `curl2httpie.online`_, but it failed with above example. So I decide to write my own tool.

I don't bother to help fix the online tool above, because it is written in Go. The rich ecosystem of Python, with these built-in libraries, enable me to finish the job fast:

- |shlex|_: Help parse the command line in form of shell language, handle the string escaping, quoting for me.
- |argparse|_: Help parse cURL options and arguments. Note that, cURL arguments syntax follow GNU style, which is common in Linux (and Python) world but not popular in Go world (see `this tutorial <go_tutorial_>`_), so it feels more natural with Python.


Usage
-----

.. code-block:: python

    >>> from curlipie import curl_to_httpie

    >>> curl = """curl -XPUT elastic.dev/movies/_doc/1 -d '{"director": "Burton, Tim", "year": 1996, "title": "Mars Attacks!"}' -H 'Content-Type: application/json'"""

    >>> curl_to_httpie(curl)
    ConversionResult(httpie="http PUT elastic.dev/movies/_doc/1 director='Burton, Tim' year:=1996 title='Mars Attacks!'", errors=[])

    >>> result = curl_to_httpie(curl)

    >>> result.httpie
    "http PUT elastic.dev/movies/_doc/1 director='Burton, Tim' year:=1996 title='Mars Attacks!'"


Online tool
-----------

CurliPie is not very usable if it stays in library form, so I made an online tool for you to use it quickly:

https://curlipie.now.sh/

The site also provide HTTP API for you to develop a client for it.


.. _cURL: https://curl.haxx.se
.. _HTTPie: https://httpie.org
.. _curl2httpie.online: https://curl2httpie.online/
.. |shlex| replace:: ``shlex``
.. _shlex: https://docs.python.org/3/library/shlex.html
.. |argparse| replace:: ``argparse``
.. _argparse: https://docs.python.org/3/library/argparse.html
.. _go_tutorial: https://gobyexample.com/command-line-flags
