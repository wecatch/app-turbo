app-turbo
=========

.. image:: https://img.shields.io/pypi/v/turbo.svg
    :alt: pip
    :target: https://pypi.python.org/pypi/turbo

.. image:: https://travis-ci.org/wecatch/app-turbo.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/wecatch/app-turbo

.. image:: https://codecov.io/github/wecatch/app-turbo/coverage.svg?branch=master
    :alt: codecov
    :target: https://codecov.io/github/wecatch/app-turbo?branch=master

.. image:: https://readthedocs.org/projects/app-turbo/badge/?version=latest
    :alt: readthedocs
    :target: https://app-turbo.readthedocs.io/en/latest/


`Turbo <http://app-turbo.readthedocs.org>`_ is a web framework for fast building web site and RESTFul api, based on tornado, mongodb, redis.


- Easily scale up and maintain
- Rapid development for RESTFul api and web site
- Django or flask application structure
- Easily customizable
- Simple ORM for mongodb
- Logger
- Session(storage support for redis, disk and so on)
- support MongoDB, MySQL, PostgreSQL and so on
- support MongoDB asynchronous driver `Motor <http://motor.readthedocs.io/en/stable/>`_ 


Getting started
----------------

.. code-block:: bash

    pip install turbo
    turbo-admin startproject <project_name>
    cd <project_name>/app-server
    touch __test__
    python main.py


Documentation
--------------

Documentation and links to additional resources are available at http://app-turbo.readthedocs.org