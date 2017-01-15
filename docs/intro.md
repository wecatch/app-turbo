# Overview

Turbo is developed for web site that based on [tornado](http://tornado.readthedocs.org/en/stable/) and [mongodb](https://www.mongodb.org/) to build rapidly and easily to scale up and maintain.


Turbo has support for:

- Easily scale up and maintain
- Rapid development for RESTFul api and web site
- Django or flask style application structure
- Easily customizing
- Simple ORM for mongodb
- Logger
- Session

In addtion to the above, turbo has a command line utility `turbo-admin` for fast build application structure.


## Demo


```sh
git clone https://github.com/wecatch/app-turbo.git
cd app-turbo/demos/helloword/app-server
python main.py
```

Open your brower and visit [http://localhost:8888](http://localhost:8888)


## Install

First be sure you have `MongoDB` and `redis` installed.


```sh
pip install turbo
```

Install the latest

```sh
git clone https://github.com/wecatch/app-turbo.git
cd app-turbo
python setup.py install
```

## Hello, world


```bash
turbo-admin startproject my_turbo_app
cd my_turbo_app
cd app-server
python main.py
```

Open your broswer and visite [http://localhost:8888](http://localhost:8888)

Server start on port 8888 default, you can change this `python main.py --port=8890`
