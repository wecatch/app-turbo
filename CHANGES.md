app-turbo changes log
=====================

## 0.4.5

**remove  methods**

model methods

```python
def get_as_column(self):
    pass

def find_and_modify(self):
    pass

def ensure_index(self):
    pass
```

**rewrite insert,update,remove**

`Insert` is replaced by `insert_one`, `update` is replaced by `update_one` and `update_many`. `Remove` is replaced with `delete_one` and `delete_many`

## 0.4.4

- add jinja2 template support

## 0.4.3

- add flux prgraming model inspired by reactjs
- add mongodb build index command line tool