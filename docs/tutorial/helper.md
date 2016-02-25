#### What is `helper`

Helper is a layer of business logic. Each package, in helpers, is a helper.


`helpers` directory skeleton

```

helpers/
   ├── wallpaper             # each package in helpers represents one mongodb databse instance
   │   ├── album.py          
   │   ├── category.py
   │   ├── image.py
   │   ├── img2tag.py
   │   ├── __init__.py       
   │   └── tag.py
   ├── __init__.py           
   ├── settings.py           # here is package needed to be installed automatically
   
```

#### Create helper

To create a helper, first create a package in helpers, for example named with `wallpaper` , and define '__all__' list attribute explicitly in  `__init__.py` file. The attribute `__all__`, it's job is to include all modules needed to be used.

```python
__all__ = ['img2tag']

```


Install helper in `helpers/setting.py`

```

INSTALLED_HELPERS = (
   'wallpaper',
)

```


#### How to use helper


import helper like this

```
from helpers import wallpaper as wallpaper_helper

```

#### How turbo instantiate helper 

Each helper is a python package. Put code bellow in package `__init__.py` file. `__all__` list includes module need to be instantiated.


```python
#wallpaper/__init__.py

__all__ = ['album', 'img2tag']

```

In each module included in `__all__`, put `Class` that need to be used into list `MODEL_SLOTS`


```python

#wallpaper/album.py

MODEL_SLOTS = ['Album', 'FavorAlbum']  

``` 

Each `Class`, for example like `Album`, both it's `Class` type and `instance` exist in helper `wallpaper` namespace.


```python

wallpaper_helper.favor_album  # import instance variable
wallpaper_helper.FavorAlbum # import Class type

```


