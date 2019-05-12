from __future__ import annotations

from typing import TYPE_CHECKING

from urllib.parse import urlparse
import json
import os

import requests

from skeema.core.dependency import Dependency
from skeema.core.container import Container

if TYPE_CHECKING:
    from typing import Any
    from skeema.core import Handle


class File(Dependency):
    def __init__(self, manager: FileManager, path: str):
        self._manager: FileManager = manager
        self._path: str = path
        self._content: str = ''
        super().__init__()

    def _populate_dependency_node(self) -> None:
        pass

    def _preload(self):
        pass

    def _postload(self):
        pass

    def load(self):
        print(f'LOADING {self._path}')

        self._preload()

        with open(self._path, 'r') as file:
            self._content = file.read()

        self._postload()

        self._populate_dependency_node()
        child_dependency_nodes = self.dependency_node.resolve_dependencies()[:-1]
        for child_dependency_node in child_dependency_nodes:
            handle: Handle = child_dependency_node.handle
            dependency: File = self._manager.get_file_from_handle(handle)
            dependency.load()


class JsonFile(File):
    def _populate_dependency_node(self) -> None:
        dependencies = JsonFile.search_definition(self._content, '$ref')
        for dependency_path in dependencies:
            url = urlparse(dependency_path)
            if url.path:
                if dependency_path.startswith('./'):
                    dependency_path = dependency_path.replace('./', f'{os.path.dirname(self._path)}\\', 1)
                dependency = self._manager.create_file(dependency_path)
                self.add_dependency(dependency)

    def _postload(self):
        self._content = json.loads(self._content)

    @staticmethod
    def search_definition(source: Any, filter_key: str) -> [str]:
        if isinstance(source, dict):
            for key, value in source.items():
                if filter_key == key:
                    yield value

                # Parse dict
                elif isinstance(value, dict):
                    for d in JsonFile.search_definition(value, filter_key):
                        yield d

                # Parse list
                elif isinstance(value, list) or isinstance(value, tuple):
                    for v in value:
                        for d in JsonFile.search_definition(v, filter_key):
                            yield d


class FileManager:
    def __init__(self):
        self._container: Container = Container()

    def create_file(self, path) -> File:
        file: File = self._create_file(path)
        self._container.add_object(path, file, path)
        return file

    def _create_file(self, path) -> File:
        pass

    def get_file_from_handle(self, handle: Handle):
        return self._container.get_object(handle)

    def load(self, path: str):
        url = urlparse(path)
        if url.scheme == 'http':
            requests.get(path)
        else:
            file = self.create_file(path)
            file.load()
            return file


class JsonFileManager(FileManager):
    def _create_file(self, path) -> File:
        return JsonFile(self, path)
