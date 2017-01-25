turbo
=========

[![Build Status](https://travis-ci.org/wecatch/app-turbo.svg?branch=master)](https://travis-ci.org/wecatch/app-turbo)


turbo 是一个用以加速建立普通 web 站点和 RESTFul api 的 framework，基于 tornado。


## 特性

- 方便扩展，易于维护
- 快速开发 web 站点 和 RESTFul api
- 类似 django 或 flask 的 app 组织结构
- 支持轻松定制特性
- 简单的 ORM，易于维护和扩展
- 灵活的 Logger
- Session (提供了对应的钩子函数，可以使用任何 storage, 自带 redis store 实现)
- 支持 MongoDB，MySQL，PostgreSQL
- 支持 MongoDB 异步驱动 Motor

## 快速开始

```
pip install turbo
turbo-admin startproject <project_name>
cd <project_name>/app-server
touch __test__
python main.py
```

## 文档


[http://app-turbo.readthedocs.org/](http://app-turbo.readthedocs.org/)

## wiki

- [我为什么创造了 turbo 这个后端的轮子](http://sanyuesha.com/2016/07/23/why-did-i-make-turbo/)
