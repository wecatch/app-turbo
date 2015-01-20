
from turbo.util import import_object
from turbo.log import helper_log
from turbo import model

class HelperObjectDict(dict):

    def __setitem__(self, name, value):
        return super(HelperObjectDict, self).setdefault(self._convert_name(name), value)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise ValueError(name)

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
        # db model package
        package = import_object('.'.join(['helpers', item]), package_space)
        package_space[item] = HelperObjectDict()
        # all py files  included by package
        all_modules = getattr(package, '__all__', [])
        for m in all_modules:
            try:
                module =  import_object('.'.join(['helpers',item, m]), package_space)
            except ImportError, e:
                raise ImportError("No module named %s in %s package" % (m, item))

            for model_name in getattr(module, 'MODEL_SLOTS', []):
                model = getattr(module, model_name, None)
                if model:
                    package_space[item][model.__name__] = model()
