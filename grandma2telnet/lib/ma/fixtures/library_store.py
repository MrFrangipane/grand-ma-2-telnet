import os.path

from grandma2telnet.lib.ma.fixtures.fixture import MAFixtureType
from grandma2telnet.lib.ma.fixtures.library import MAFixtureLibrary
from grandma2telnet.lib.ma.installation_store import MAInstallationStore


class MAFixtureLibraryStore:
    def __init__(self):
        self.libraries: dict[str, MAFixtureLibrary] = dict()
        self._installation_store = MAInstallationStore()

    def list_libraries(self):
        self.libraries = dict()
        self._installation_store.list_installations()
        for installation in self._installation_store.installations.values():
            self.libraries[installation.version] = MAFixtureLibrary(version=installation.version)

    def load_library(self, version: str):
        if version not in self.libraries:
            raise ValueError(f"Library version {version} not found")

        library_path = self._installation_store.installations[version].library
        for item in sorted(os.listdir(library_path)):
            basename, _ = os.path.splitext(item)
            try:
                manufacturer, name, mode = basename.split("@")
                self.libraries[version].fixtures.append(MAFixtureType(
                    manufacturer=manufacturer.replace("_", " ").capitalize(),
                    name=name.replace("_", " ").capitalize(),
                    mode=mode.replace("_", " ").capitalize(),
                ))
            except ValueError:
                pass


if __name__ == '__main__':
    from pprint import pprint

    fixture_library_store = MAFixtureLibraryStore()
    fixture_library_store.list_libraries()
    fixture_library_store.load_library(list(fixture_library_store.libraries.values())[0].version)

    fixtures = list(fixture_library_store.libraries.values())[0].fixtures
    pprint(fixtures)
