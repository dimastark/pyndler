import ast
import codecs
import pkgutil
import re

from os import path


def escape(string):
    encoder = codecs.getencoder('unicode_escape')
    string = encoder(string)[0].decode('ascii')

    return '"""{0}"""'.format(string)


class ImportTarget:
    def __init__(self, absolute_path, module_path):
        self.absolute_path = absolute_path
        self.module_path = path.normpath(module_path)

    def read(self):
        with open(self.absolute_path) as f:
            return f.read()

    def imports(self):
        tree = ast.parse(self.read(), self.absolute_path)

        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue

            names = [a.name for a in node.names]

            if isinstance(node, ast.Import):
                yield from map(ImportLine.with_name, names)

            if isinstance(node, ast.ImportFrom):
                yield ImportLine(node.module or '.', names)


class ImportLine:
    builtins = [m.name for m in pkgutil.iter_modules()]

    def __init__(self, import_path, items):
        import_path = import_path.replace('.', '/')
        import_path = re.sub('^/', './', import_path)

        self.import_path = import_path
        self.items = items

    @property
    def is_builtin(self):
        return self.import_path in self.builtins

    @staticmethod
    def with_name(name):
        return ImportLine(name, [])


class ModuleWriterGenerator:
    def __init__(self, sys_path):
        self._sys_path = sys_path
        self.modules = {}

    def build(self):
        return ''.join([
            f'__pyndler__.write_module({escape(module_path)}, {escape(module_source)})\n'
            for module_path, module_source in self.modules.items()
        ])

    def generate_for_file(self, python_file_path):
        self._generate_for_module(ImportTarget(python_file_path, '.'))

    def _generate_for_module(self, python_module):
        for import_line in python_module.imports():
            if not import_line.is_builtin:
                self._generate_for_import(python_module, import_line)

    def _generate_for_import(self, python_module, import_line):
        import_targets = self._read_possible_import_targets(python_module, import_line)

        for import_target in import_targets:
            if import_target.module_path not in self.modules:
                self.modules[import_target.module_path] = import_target.read()
                self._generate_for_module(import_target)

    def _read_possible_import_targets(self, python_module, import_line):
        import_path_parts = import_line.import_path.split('/')
        possible_init_module_paths = [
            path.join(path.join(*import_path_parts[0:index + 1]), '__init__.py')
            for index in range(len(import_path_parts))
        ]

        possible_module_paths = [import_line.import_path + '.py'] + possible_init_module_paths

        for item in import_line.items:
            possible_module_paths += [
                path.join(import_line.import_path, item + '.py'),
                path.join(import_line.import_path, item, '__init__.py')
            ]

        import_targets = [
            self._find_module(python_module, module_path)
            for module_path in possible_module_paths
        ]

        valid_import_targets = [target for target in import_targets if target is not None]
        return valid_import_targets

    def _find_module(self, importing_python_module, module_path):
        relative_module_path = path.join(path.dirname(importing_python_module.absolute_path), module_path)
        if path.exists(relative_module_path):
            return ImportTarget(relative_module_path,
                                path.join(path.dirname(importing_python_module.module_path), module_path))

        full_module_path = path.join(self._sys_path, module_path)
        if path.exists(full_module_path):
            return ImportTarget(full_module_path, module_path)
