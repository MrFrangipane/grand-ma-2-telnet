import os
import shutil

import time
from tempfile import NamedTemporaryFile

from grandma2telnet.lib.ma.filesystem import FileSystem
from grandma2telnet.lib.ma.installation import Installation
from grandma2telnet.lib.ma.low_level_api import LowLevelApi


class MA:

    def __init__(self, host: str):
        self._low_level_api = LowLevelApi(host=host)
        self._filesystem = FileSystem()
        self._filesystem.list_installations()
        self._installation: Installation |  None = None

    @property
    def versions(self) -> list[str]:
        return list(self._filesystem.installations.keys())

    def set_version(self, version: str):
        if version not in self.versions:
            raise ValueError(f"Version {version} not found")

        self._installation = self._filesystem.installations[version]
        print(f"Selected installation {self._installation.version}")

    def connect(self, username: str, password: str):
        self._low_level_api.connect()
        self._low_level_api.login(username, password)

    def disconnect(self):
        self._low_level_api.disconnect()

    def add_fixture_type(self, fixture_type_name: str):
        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest('EditSetup/FixtureTypes')
        self._low_level_api.import_(fixture_type_name)

    def import_fixture_type(self, filepath: str):
        self._import_file(filepath, "library", "EditSetup/FixtureTypes")

    def import_fixtures(self, filepath: str):
        self._import_file(filepath, "fixture_layers", "EditSetup/Layers", position=1, cleanup=True)

    # FIXME move to low lovel API ? (or create a "mid-level" one ?)
    def _import_file(self, filepath: str, installation_folder: str, destination: str, position: int | None = None, cleanup: bool = False):
        if self._installation is None:
            raise ValueError("Installation not set")

        filename = os.path.splitext(os.path.basename(filepath))[0]
        file_destination = os.path.join(getattr(self._installation, installation_folder), filename + ".xml")

        shutil.copy(filepath, file_destination)

        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest(destination)
        self._low_level_api.import_(filename, position=position)

        self._low_level_api.change_dest("/")

        if cleanup:
            os.remove(file_destination)
