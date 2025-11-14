import os.path

from grandma2telnet.lib.fixtures.fixture import Fixture
from grandma2telnet.lib.fixtures.library import Library


class FixtureLibraryStore:
    def __init__(self):
        self.libraries: dict[str, Library] = dict()
        self._list_installed_libraires()

    def _list_installed_libraires(self):
        self.libraries = dict()

        root_installation_path = os.path.expandvars("%programdata%\\MA Lighting Technologies\\grandma")
        if not os.path.exists(root_installation_path):
            raise FileNotFoundError(f"Installation path {root_installation_path} does not exist")

        for item in os.listdir(root_installation_path):
            if os.path.isdir(os.path.join(root_installation_path, item)) and item.startswith("gma2_"):
                version = item.split("_")[-1]
                self.libraries[version] = Library(
                    version=version,
                    fullpath=os.path.join(root_installation_path, item, 'library')
                )

    def load_library(self, version: str):
        if version not in self.libraries:
            raise ValueError(f"Library version {version} not found")

        for item in sorted(os.listdir(self.libraries[version].fullpath)):
            basename, _ = os.path.splitext(item)
            try:
                manufacturer, name, mode = basename.split("@")
                self.libraries[version].fixtures.append(Fixture(
                    manufacturer=manufacturer.replace("_", " ").capitalize(),
                    name=name.replace("_", " ").capitalize(),
                    mode=mode.replace("_", " ").capitalize(),
                ))
            except ValueError:
                pass

if __name__ == '__main__':
    from pprint import pprint

    fixture_library_store = FixtureLibraryStore()
    fixture_library_store.load_library(list(fixture_library_store.libraries.values())[0].version)

    fixtures = list(fixture_library_store.libraries.values())[0].fixtures
    for fixture in fixtures:
        if fixture.manufacturer.lower() == "BeamZ".lower() and \
            fixture.name.lower() == "Nereid380B".lower() and \
            fixture.mode.lower() == "Standard 1.2".lower():
            print(fixture)
