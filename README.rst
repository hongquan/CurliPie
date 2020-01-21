========
CurliPie
========


Python library to convert `cURL`_ command to `HTTPie`_.

It will convert

.. code-block:: sh

    curl -d name=admin -d shoesize=12 -d color=green&food=wet http://quan.hoabinh.vn

to

.. code-block:: sh

    http -f http://quan.hoabinh.vn name=admin shoesize=12 color=green food=wet


.. _cURL: https://curl.haxx.se
.. _HTTPie: https://httpie.org
