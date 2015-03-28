# 介绍

turbo 的诞生旨在为基于 [tornado](http://tornado.readthedocs.org/en/stable/) 和 [mongodb](https://www.mongodb.org/) 的应用开发提供**快速构建**，**便于扩展**，**易于维护**的最佳实践方案。turbo 包含以下特性

- 简易的 orm (基于mongodb) 
- 快速构建 rest api
- 易于扩展和维护的app结构
- 灵活的 log 

# 用 turbo 构建应用的目录结构

```

	├── app-server
	├── conf
	├── db
	├── helpers
	├── models

```

## app-server 

业务层，目录结构如下

```

	├── apps
	│   ├── base.py
	│   ├── __init__.py
	│   ├── settings.py
	│   └── user
	├── main.py
	├── setting.py

```

**main.py**

这是应用的入口模块，负责启动应用


**setting.py**

app-server 的配置文件，包含 tornado 和 app-server 的配置


**apps**


 应用的业务层，由不同的子 app 组成












