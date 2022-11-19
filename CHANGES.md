app-turbo changes log
=====================

## 0.5.0

- fix file upload bug in Python3

## 0.4.8

- Support Python3.4, Python3.5, Python3.6

## 0.4.7

- Support turbo in Python 2.7 install correctly

## 0.4.5

- Methods `get_as_column`,`create`, attribute `column` are removed from `BaseModel` class
- Move tests outside turbo package
- Rewrite insert,update,remove with the latest pymongo collection methods like `insert_one`,`insert_many` and so on.
- `BaseModel` method `inc` add multi docs support
- add `mongo_model` module for support [motor](http://motor.readthedocs.io/en/stable/)

**warning**

4.5 从 `BaseModel` 中弃用了 `create` 方法，请使用 `insert` 代替，默认所有插入操`insert`,`insert_one`,`insert_many`,`save` 都会进行 `field` 属性中键的校验，可以使用关键字参数 `check=False` 跳过校验。

4.5 为了支持异步 mongo 驱动 `motor` pymongo 必须 >=3.2，请谨慎升级安装。

## 0.4.4

- add jinja2 template support

## 0.4.3

- add flux prgraming model inspired by reactjs
- add mongodb build index command line tool
