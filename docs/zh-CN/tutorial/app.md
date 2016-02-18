#### 什么是 app-server

app-server 是 web 应用程序，由一个或多个子 app 组成，每个 app 结构独立，可移植，可复用


####  app-server 的目录结构示例


``` sh

    app-server/
    ├── apps
    │   ├── base.py
    │   ├── __init__.py
    │   ├── settings.py                # base.py 使用的配置
    │   └── user                       # 子 app user
    │       ├── app.py
    │       ├── base.py
    │       ├── __init__.py
    │       ├── setting.py
    ├── main.py                        # 入口
    ├── setting.py                     # 应用配置
    ├── templates                      # 模板
    │   └── user
    │       └── index.html
    ├── static                         # 静态文件
    │   └── js
    │       └── jquery.js


```


#### 建立 model


使用 turbo 的命令行工具建立 app-server

```sh

turbo-admin startserver  app-server

```


#### 启动app-server

```

python main.py

```

