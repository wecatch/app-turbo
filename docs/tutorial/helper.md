#### What is `helper`

Helper is business lagic layer.


`helpers` directory skeleton

```

helpers/
   ├── wallpaper             # mongodb databse instance mappig, one instance helper
   │   ├── album.py          
   │   ├── category.py
   │   ├── image.py
   │   ├── img2tag.py
   │   ├── __init__.py       
   │   └── tag.py
   ├── __init__.py           
   ├── settings.py           
   
```

#### Create helper

In helpers package, create package that `__init__.py` with `__all__` list attribute explicitly.

Put `module` in `__all__` list

Install helper in helpers/setting.py

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

Each `Class` like `Album`, both it's `Class` type and `instance` exist in helper `wallpaper` namespace.


```python

wallpaper_helper.favor_album  # import instance variable
wallpaper_helper.FavorAlbum # import Class type

```


