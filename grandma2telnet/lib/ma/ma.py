import re
import os
import shutil
import logging

from grandma2telnet.lib.ma.filesystem import FileSystem
from grandma2telnet.lib.ma.fixtures.fixture import Fixture
from grandma2telnet.lib.ma.installation import Installation
from grandma2telnet.lib.ma.low_level_api import LowLevelApi
from pythonhelpers.vector import Vector3

_logger = logging.getLogger("MA")
_RE_LIST_LAYERS = re.compile(pattern=r'Layer (\d+) ([^\[\(]+)')


class MA:

    def __init__(self, host: str, username: str | None = None, password: str | None = None):
        self._low_level_api = LowLevelApi(host=host)
        self._filesystem = FileSystem()
        self._filesystem.list_installations()
        self._installation: Installation |  None = None

        if username is not None and password is not None:
            self.connect(username, password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def installations(self) -> list[str]:
        return list(self._filesystem.installations.keys())

    def set_installation(self, version: str):
        if version not in self.installations:
            raise ValueError(f"Version {version} not found")

        self._installation = self._filesystem.installations[version]
        _logger.info(f"Selected installation {self._installation.version}")

    def connect(self, username: str, password: str):
        self._low_level_api.connect()
        self._low_level_api.login(username, password)

    def disconnect(self):
        self._low_level_api.disconnect()

    def add_fixture_type(self, fixture_type_name: str):
        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest('EditSetup/FixtureTypes')
        self._low_level_api.import_(fixture_type_name)
        self._low_level_api.change_dest("/")

    def import_fixture_type(self, filepath: str):
        self._import_file(filepath, "library", "EditSetup/FixtureTypes")

    def import_fixtures(self, filepath: str):
        self._import_file(filepath, "fixture_layers", "EditSetup/Layers", position=1, cleanup=True)

    def set_fixture_type(self, fixture_type_id: int, fixture_first: int, fixture_last: int | None = None):
        self._low_level_api.change_dest('EditSetup')
        self._low_level_api.set_fixture_type(fixture_type_id, fixture_first, fixture_last)
        self._low_level_api.change_dest("/")

    def list_layers(self) -> dict[int, str]:
        self._low_level_api.change_dest('EditSetup/Layers')
        table_parser = self._low_level_api.list_layers()
        self._low_level_api.change_dest("/")

        layers = dict()
        for line in table_parser.lines:
            found = _RE_LIST_LAYERS.findall(line['Name'])
            if found:
                layers[int(found[0][0])] = found[0][1]

        return layers

    def list_fixtures(self, layer_id: int) -> dict[int, Fixture]:
        self._low_level_api.change_dest(f'EditSetup/Layers/{layer_id}')
        table_parser = self._low_level_api.list_fixtures(layer_id)
        self._low_level_api.change_dest("/")

        fixtures = dict()
        for line in table_parser.lines:
            fixture_id = int(line['FixId'])
            universe_str, channel_str = line['Patch'].split('.')
            fixtures[fixture_id] = Fixture(
                id=fixture_id,
                name=line['Name'],
                type=line['FixtureType'],  # FIXME: get from library !!
                universe=int(universe_str),
                channel=int(channel_str),
                position=Vector3(x=float(line['PosX']), y=float(line['PosY']), z=float(line['PosZ'])),
                rotation=Vector3(x=float(line['RotX']), y=float(line['RotY']), z=float(line['RotZ'])),
            )

        return fixtures

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
