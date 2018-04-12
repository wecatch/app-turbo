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
- Support MongoDB, MySQL, PostgreSQL and so on
- Support MongoDB asynchronous driver [Motor](http://motor.readthedocs.io/en/stable/) base on [turbo-motor](https://github.com/wecatch/turbo-motor)
- Support Python3

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

## Tutorial

- [让 turbo 支持异步调用 MongoDB](http://sanyuesha.com/2018/04/11/turbo-motor/)
- [turbo 的诞生记](http://sanyuesha.com/2016/07/23/why-did-i-make-turbo/)
