import subprocess as sp
import tempfile

from os import path

import pytest

import pyndler


@pytest.mark.parametrize('script_path,expected_output', [
    ('circular_reference', 'a\n'),
    ('explicit_relative_import', 'a\n'),
    ('explicit_relative_import_single_dot', 'a\n'),
    ('implicit_init_import', 'a\n'),
    ('import_from_as_module', 'a\n'),
    ('import_from_as_value', 'a\n'),
    ('imports_in_imported_modules', 'a\n'),
    ('script_using_from_to_import_module', 'a\n'),
    ('script_using_from_to_import_multiple_modules', 'a\n'),
    ('script_using_from_to_import_multiple_values', 'a\n'),
    ('script_using_module_in_package', 'a\n'),
    ('script_with_single_local_from_import', 'a\n'),
    ('script_with_single_local_import', 'a\n'),
    ('script_with_single_local_import_of_package', 'a\n'),
    ('single_file', 'a\n'),
    ('single_file_using_stdlib', '86f7e437faa5a7fce15d1ddcb9eaeaea377667b8\n'),
])
def test_pyndler(script_path: str, expected_output: str):
    assert run_bundle(path.join(script_path, 'entry')) == expected_output


def run_bundle(script_path: str) -> str:
    scripts_dir = path.join(path.dirname(__file__), 'scripts')
    result = pyndler.bundle(path.join(scripts_dir, script_path))

    with tempfile.NamedTemporaryFile('w') as tf:
        tf.write(result)
        tf.flush()

        return sp.run(['python3', tf.name], stdout=sp.PIPE, encoding='utf-8').stdout
