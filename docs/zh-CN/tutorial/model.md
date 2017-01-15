#### 什么是model

model 是 mongodb collection 的简单反射，它包含了 collection 中每个 record 字段和类型的简单描述，方便在开发过程中对其进行查阅和更改。model 继承自turbo.model 的 BaseModel，BaseModel 封装了 pymongo 的基础操作和 api。


#### model的目录结构

```
models
├── __init__.py  
├── settings.py            # model 的全局配置, 数据库连接等的配置
├── base.py                # 各个db 所需要的数据库映射配置初始化, 继承model所需要的 collection 操作等
├── user  
│   ├── __init__.py
│   ├── base.py            # 每个 model 连接的 db 指定
│   ├── model.py           # model 对应 db 的所有 colletion 结构
│   └── setting.py         # 每个 model 具体的配置

```


#### 建立 model

在 models 目录下面建立model对应的package, 包含以下模块

* __init__.py
* base.py
* setting.py
* model.py


在 **base.py** 中 建立 model 对应的 db 配置

```python

# base.py

from models.base import *

class Model(BaseModel):

    def __init__(self):
        super(Model, self).__init__(db_name='user')

```


在 model.py 中声明相应的model 即可

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

#### 在 helper 中使用 model

```python

from models.user import model

class User2img(model.User2img):pass

```
