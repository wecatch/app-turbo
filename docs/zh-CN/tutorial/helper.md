#### 什么是**helper**

helper是提供业务逻辑的层次，它继承了基础 model，在已经封装好的 pymongo api(find, find_one, insert, inc等)上进行相应的业务逻辑封装。

只需要按照规则进行配置，helper 就可以实现自动化声明和导入。

#### **helper**的目录结构示例

```

helpers/
   ├── wallpaper             # 相应db的package，即一个具体的helper
   │   ├── album.py          # 封装了对应model业务逻辑的模块
   │   ├── category.py
   │   ├── image.py
   │   ├── img2tag.py
   │   ├── __init__.py       # 模块的内建属性__all__ 中配置需要导入的module
   │   └── tag.py
   ├── __init__.py           # 自动导入helper 目录下面的 helper
   ├── settings.py           # helper 中用到的全局公有变量和helper安装列表

```

#### helper 使用说明

应用程序启动之后，在app-server的任意地方，以下面的方式导入helper


```
from helpers import wallpaper as wallpaper_helper

```

#### helper 是如何实现在外部被引用的

在 helpers 目录下的每个的 helper 中，例如 wallpaper, 其 **__init__.py** 的 **__all__** 属性中指定所有需要导出的模块，例如

```python

# __init__.py

__all__ = ['album', 'img2tag']  # 导出 album.py 和 img2tag.py

```

在要导出的模块中通过 **MODEL_SLOTS** 属性指定导出的类， 例如


```python

#album.py

MODEL_SLOTS = ['Album', 'FavorAlbum']  # 导出 album.py 中的 Album 和 FavorAlbum 类

```


每个导出的类都将以**实例**和**类**变量两种形式存在于所在的 helper 的命名空间中，实例变量的的名称被自动转换为 underscore 模式，例如


```python

wallpaper_helper.favor_album  # 访问实例变量
wallpaper_helper.FavorAlbum # 访问类变量

```

在 helpers/setting.py 中指定导出的helper


```

INSTALLED_HELPERS = (
   'wallpaper',
)

```

至此，导出一个helper 完成
