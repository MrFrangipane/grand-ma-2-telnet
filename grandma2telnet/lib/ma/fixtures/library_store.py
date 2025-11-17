import os.path

from grandma2telnet.lib.ma.filesystem import FileSystem
from grandma2telnet.lib.ma.fixtures.fixture import FixtureType
from grandma2telnet.lib.ma.fixtures.library import FixtureLibrary


class FixtureLibraryStore:
    def __init__(self):
        self.libraries: dict[str, FixtureLibrary] = dict()
        self._filesystem = FileSystem()

    def list_libraries(self):
        self.libraries = dict()
        self._filesystem.list_installations()
        for installation in self._filesystem.installations.values():
            self.libraries[installation.version] = FixtureLibrary(version=installation.version)

    def load_library(self, version: str):
        if version not in self.libraries:
            raise ValueError(f"Library version {version} not found")

        library_path = self._filesystem.installations[version].library
        for item in sorted(os.listdir(library_path)):
            basename, _ = os.path.splitext(item)
            try:
                manufacturer, name, mode = basename.split("@")
                self.libraries[version].fixtures.append(FixtureType(
                    manufacturer=manufacturer.replace("_", " ").capitalize(),
                    name=name.replace("_", " ").capitalize(),
                    mode=mode.replace("_", " ").capitalize(),
                ))
            except ValueError:
                pass

if __name__ == '__main__':
    from pprint import pprint

    fixture_library_store = FixtureLibraryStore()
    fixture_library_store.list_libraries()
    fixture_library_store.load_library(list(fixture_library_store.libraries.values())[0].version)

    fixtures = list(fixture_library_store.libraries.values())[0].fixtures
    pprint(fixtures)
