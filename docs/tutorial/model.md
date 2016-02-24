#### What is `model`

Instance of model `Class` represents mongodb collection, model defines the collection schema.


`models` directory skeleton

```
models
├── __init__.py         
├── settings.py            # global setting for all models
├── base.py                # mongodb database instance mappings
├── user                   
│   ├── __init__.py
│   ├── base.py            
│   ├── model.py           # all model Class, each represents one mongodb collection
│   └── setting.py         # setting for user model

```


#### Create model

In models package create package `user` like bellow


```bash
user
├──__init__.py
├── base.py            
├── model.py           
└── setting.py  

```


Put code in `base.py`

```python

# base.py 

from models.base import * 

class Model(BaseModel):

    def __init__(self):
        super(Model, self).__init__(db_name='user')

```


Create `Class` inherited from `turbo.model.BaseModel`

```
from base import *

class User2img(Model): 

    name = 'user2img'      # collection 的名字

    field = {
        'uid':             (ObjectId, None)    ,
        'imgid':           (ObjectId, None)    ,
        'atime':           (datetime, None)    ,
        'atime':           (datetime, None)    ,
    }

```

#### Use model in helper

```python
#helpers/user/user.py
from models.user import model

class User2img(model.User2img):pass

```
