import logging
import os
import re
import shutil

from grandma2telnet.lib.ma.console_selection_info import MAConsoleSelectionInfo
from grandma2telnet.lib.ma.fixtures.fixture import MAFixture
from grandma2telnet.lib.ma.installation import MAInstallation
from grandma2telnet.lib.ma.low_level_api import LowLevelApi

_logger = logging.getLogger("MA")
_RE_LIST_LAYERS = re.compile(pattern=r'Layer (\d+) ([^\[\(]+)')


class MAConsole:
    def __init__(self, connection_info: MAConsoleSelectionInfo | None = None):
        self.console_selection_info = connection_info

        self._low_level_api: LowLevelApi | None = None
        self._installation: MAInstallation | None = None

        if self.console_selection_info is not None:
            self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def is_connected(self):
        return self._low_level_api is not None

    def set_installation(self, installation: MAInstallation):
        self._installation = installation
        self.console_selection_info.version = installation.version
        _logger.info(f"Selected installation {installation.version}")

    def connect(self):
        self._low_level_api = LowLevelApi(self.console_selection_info.host)
        self._low_level_api.connect()
        self._low_level_api.login(self.console_selection_info.username, self.console_selection_info.password)

    def disconnect(self):
        self._low_level_api.disconnect()
        self._low_level_api = None

    def add_fixture_type(self, fixture_type_name: str):
        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest('EditSetup/FixtureTypes')
        self._low_level_api.import_(fixture_type_name)
        self._low_level_api.change_dest("/")

    def import_fixture_type(self, filepath: str):
        self._import_file(filepath, "library", "EditSetup/FixtureTypes")

    def import_fixtures(self, filepath: str):
        self._import_file(filepath, "fixture_layers", "EditSetup/Layers", position=1, cleanup=True)

    def export_fixtures(self, filepath: str):
        self._export_file(filepath, "fixture_layers", "EditSetup/Layers")

    def set_fixture_type(self, layer_id: int, fixture_type_id: int, fixture_first: int, fixture_last: int | None = None):
        self._low_level_api.change_dest(f'EditSetup/Layers/{layer_id + 1}')
        self._low_level_api.set_fixture_type(fixture_type_id, fixture_first, fixture_last)
        self._low_level_api.change_dest("/")

    def list_layers(self) -> dict[int, str]:
        self._low_level_api.change_dest('EditSetup/Layers')
        table_parser = self._low_level_api.list_and_parse_table()
        self._low_level_api.change_dest("/")

        layers = dict()
        for line in table_parser.lines[1:]:
            if 'Name' not in line:
                table_parser.print_debug()
                raise ValueError("Could not parse layers")

            found = _RE_LIST_LAYERS.findall(line.get('Name', ''))
            if found:
                layers[int(found[0][0]) - 1] = found[0][1]

        return layers

    def delete_layers(self, first: int | None = None, last: int | None = None):
        if first is None:
            first = 1

        self._low_level_api.change_dest('EditSetup/Layers')
        self._low_level_api.delete(first + 1, last + 1)
        self._low_level_api.change_dest("/")

    def delete_all_layers(self):
        self.delete_layers(last=len(self.list_layers()))

    def list_fixtures(self, layer_id: int) -> list[MAFixture]:
        self._low_level_api.change_dest(f'EditSetup/Layers/{layer_id + 1}')
        table_parser = self._low_level_api.list_and_parse_table()
        self._low_level_api.change_dest("/")

        fixtures = list()
        for line in table_parser.lines:
            fixture_id = int(line['FixId']) if line['FixId'] != '-' else None
            if line['Patch'] == '(-)':
                universe_str, channel_str = None, None
            else:
                universe_str, channel_str = line['Patch'].split('.')

            fixtures.append(MAFixture(
                id=fixture_id,
                name=line['Name'],
                type=line['FixtureType'],  # FIXME: get from library !!
                layer_id=layer_id,
                universe=int(universe_str) if universe_str is not None else None,
                channel=int(channel_str) if channel_str is not None else None,
            ))

        return fixtures

    def clear_patch(self):
        self._low_level_api.clear_patch()

    def set_fixture_patch(self, fixture_id: int, patch: str):
        self._low_level_api.set_fixture_patch(fixture_id, patch)

    # FIXME move to low lovel API ? (or create a "mid-level" one ?)
    def _import_file(self, filepath: str, installation_folder: str, destination: str, position: int | None = None, cleanup: bool = False):
        if self._installation is None:
            raise ValueError("Installation not set")

        filename = os.path.splitext(os.path.basename(filepath))[0]
        installation_filepath = os.path.join(getattr(self._installation, installation_folder), filename + ".xml")

        shutil.copy(filepath, installation_filepath)

        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest(destination)
        self._low_level_api.import_(filename, position=position)

        self._low_level_api.change_dest("/")

        if cleanup:
            os.remove(installation_filepath)

    def _export_file(self, filepath: str, installation_folder: str, destination: str, cleanup: bool = False):
        if self._installation is None:
            raise ValueError("Installation not set")

        filename = os.path.splitext(os.path.basename(filepath))[0]
        installation_filepath = os.path.join(getattr(self._installation, installation_folder), filename + ".xml")

        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest(destination)
        self._low_level_api.export(filename)

        self._low_level_api.change_dest("/")

        shutil.copy(installation_filepath, filepath)
        if cleanup:
            os.remove(installation_filepath)
