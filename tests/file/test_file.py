import pytest
import os
from urllib.parse import urljoin

from skeema.file.file import JsonFileManager, JsonFile


class TestFile:
    pass


class TestFileManager:
    class TestLoad:
        def test_loads_a_local_file(self):
            file_manager = JsonFileManager()
            cwd = os.getcwd()
            scheme = 'file://'
            path = f'{cwd}\\test_files\\address_schema.json'
            p = urljoin(scheme, path)
            print(p)
            file_manager.load(p)
