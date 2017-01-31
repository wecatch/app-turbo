turbo
=========

[中文文档](https://github.com/wecatch/app-turbo/blob/master/zh-CN_README.md)

[![pypi](https://img.shields.io/pypi/v/turbo.svg)](https://pypi.python.org/pypi/turbo)
[![Build Status](https://travis-ci.org/wecatch/app-turbo.svg?branch=master)](https://travis-ci.org/wecatch/app-turbo)
[![codecov](https://codecov.io/github/wecatch/app-turbo/coverage.svg?branch=master)](https://codecov.io/github/wecatch/app-turbo?branch=master)
[![readthedocs](https://readthedocs.org/projects/app-turbo/badge/?version=latest)](https://app-turbo.readthedocs.io/en/latest/)


Turbo is a framework for fast building web site and RESTFul api, based on tornado.


- Easily scale up and maintain
- Rapid development for RESTFul api and web site
- Django or flask application structure
- Easily customizable
- Simple ORM for MongoDB
- Logger
- Session(storage support for redis, disk and so on)
- support MongoDB, MySQL, PostgreSQL and so on
- support MongoDB asynchronous driver [Motor](http://motor.readthedocs.io/en/stable/)

**Prerequisites**: Turbo now only runs on Python 2.x, Python 3 support will be added in future.

## Getting started

```
pip install turbo
turbo-admin startproject <project_name>
cd <project_name>/app-server
touch __test__
python main.py
```

## Documentation

Documentation and links to additional resources are available at [http://app-turbo.readthedocs.org/](http://app-turbo.readthedocs.org/)

