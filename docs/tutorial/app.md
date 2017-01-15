#### What is app-server

App-server is a web application, be made of one or more sub app, each sub app easily migrited and resue


`app-server` directory skeleton


``` sh

    app-server/
    ├── apps
    │   ├── base.py
    │   ├── __init__.py
    │   ├── settings.py  
    │   └── user                       # sub app user
    │       ├── app.py
    │       ├── base.py
    │       ├── __init__.py
    │       ├── setting.py
    ├── main.py                        # entry
    ├── setting.py  
    ├── templates  
    │   └── user
    │       └── index.html
    ├── static  
    │   └── js
    │       └── jquery.js


```


#### Create app-server


```sh
turbo-admin startserver  app-server
cd app-server
python main.py
```




