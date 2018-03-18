#!/usr/bin/env python


class __pyndler__:
    import re
    from importlib.abc import SourceLoader

    py_re = re.compile('(\.py|/__init__\.py)$')
    finder = None

    def __init__(self):
        import sys
        finder = __pyndler__.Finder()
        __pyndler__.finder = finder
        sys.meta_path.insert(2, finder)

    class Finder:
        def __init__(self):
            self.modules = {}
            self.packages = set()

        def find_module(self, module_name, package_path):
            if module_name in self.modules:
                return __pyndler__.Loader(self.modules, self.packages)

    class Loader(SourceLoader):
        def __init__(self, modules, packages):
            self.modules = modules
            self.packages = packages

        def get_filename(self, fullname):
            return fullname

        def module_repr(self, module):
            return repr(module)

        def get_data(self, path):
            if path not in self.modules:
                raise IOError

            return self.modules[path]

        def is_package(self, fullname):
            return fullname in self.packages

    @staticmethod
    def write_module(path, contents):
        module_path = __pyndler__.py_re.sub('', path)
        module_path = module_path.replace('/', '.')
        __pyndler__.finder.modules[module_path] = contents.encode()
        if path.endswith('__init__.py'):
            __pyndler__.finder.packages.add(module_path)


__pyndler__()
