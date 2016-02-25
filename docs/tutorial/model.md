#### What is `model`


Model has two meanings, one means `model Class`, the other means package which encapsulates `model.py`

`model Class` represents mongodb collection and defines the collection schema.


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


To create a model, first create a package below in models, for example named with `user`.


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
from base import *         # import BaseModel from base

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
