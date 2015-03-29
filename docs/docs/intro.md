# 介绍

turbo 的诞生旨在为基于 [tornado](http://tornado.readthedocs.org/en/stable/) 和 [mongodb](https://www.mongodb.org/) 的应用开发提供**快速构建**，**便于扩展**，**易于维护**的最佳实践方案。turbo 包含以下特性

- 简易的 orm (基于mongodb) 
- 快速构建 rest api
- 易于扩展和维护的app结构
- 灵活的 log 

# turbo 构建的应用

目录结构

```

	├── app-server
	├── conf
	├── db
	├── helpers
	├── models

```

## app-server 

    
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


应用的业务层，由不同的子 app 组成，每个子 app 都是独立存在的，**可移植**，**可复用**



## models


```

	├── base.py
	├── __init__.py
	├── settings.py
	└── user
	    ├── base.py
	    ├── __init__.py
	    ├── model.py
	    └── setting.py

```

**base.py**

数据库连接的映射以及 models 的全局方法

**settings.py**

数据库连接和引用


**user package**

子 model，一般对应一个 db



## helpers 

目录结构


```

	helpers/
	   ├── user         
	   │   ├── user.py          
	   │   ├── __init__.py      
	   │   └── tag.py
	   ├── __init__.py           
	   ├── settings.py         

```




**settings.py**


子 helper 安装列表


**user package**

子 helper



# demo


```

git clone https://github.com/wecatch/app-turbo.git

cd app-turbo/demos/helloword/app-server

python main.py  

```

打开浏览器，访问[http://localhost:8888](http://localhost:8888)




