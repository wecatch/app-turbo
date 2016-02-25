Tutorial
=================

Turbo application directory tree skeleton is below:

```
├── app-server
├── conf
├── db
├── helpers
├── models
└── test
```

[models](model) is made of datebase sechema, each package in `models` represents one mongodb databse instance.  

[app-server](app-server) is a web app, not python package, turbo application can have one or many app-server, each with different name.

[helpers](helpers) is model instance, responsible for business logic.

`db` is support for mongodb connections
