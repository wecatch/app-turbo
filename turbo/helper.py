from tornado.util import import_object

from turbo.log import helper_log

class HelperObjectDict(dict):

    def __setitem__(self, name, value):
        self[self._convert_name[name]] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise ValueError(name)

    def __setattr__(self, name, value):
        self[self._convert_name(name)] = value

    def _convert_name(self, name):
        """
        convert CamelCase style to under_score_case
        """
        as_list = []
        length = len(name)
        for index, i in enumerate(name):
            if index !=0 and index != length-1 and i.isupper():
                as_list.append('_%s'%i.lower())
            else:
                as_list.append(i.lower())

        return ''.join(as_list)


def install_helper(installing_helper_list, package_space):
    for item in installing_helper_list:
        helper_package = import_object('helpers'+'.'+item)
        package_space[item] = HelperObjectDict()
        
        for hp in getattr(helper_package, '__all__', []):
            try:
                module =  import_object('.'.join(['helpers', item, hp]))
            except ImportError:
                raise ImportError("No module named %s in %s package" % (hp, item))

            for m in getattr(module, 'MODEL_SLOTS', []):
                try:
                    model = getattr(module, m, None)
                except AttributeError:
                    raise ImportError("No model named %s in %s module" % (m, module))

                package_space[item][model.__name__] = model()

