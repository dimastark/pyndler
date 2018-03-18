from os import path

from pyndler.writer import ModuleWriterGenerator


def bundle(entry_path):
    prefix = read_prefix()
    entry = read_entry(entry_path)
    modules = read_modules(entry_path)

    return ''.join([prefix, modules, entry])


def read_prefix():
    prefix_path = path.join(path.dirname(__file__), 'prefix.py')

    with open(prefix_path) as prefix_file:
        return prefix_file.read()


def read_entry(entry_path):
    with open(entry_path) as entry_file:
        return entry_file.read()


def read_modules(entry_path):
    sys_path = path.dirname(entry_path)
    generator = ModuleWriterGenerator(sys_path)
    generator.generate_for_file(entry_path)

    return generator.build()
