import csv
import logging

from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from grandma2telnet.lib.ma.console import MAConsole
from grandma2telnet.lib.ma.console_selection_info import MAConsoleSelectionInfo
from grandma2telnet.lib.ma.fixtures.fixture import MAFixture
from grandma2telnet.lib.session.repatch_info import RepatchInfo


_logger = logging.getLogger("Session")


@dataclass_json
@dataclass
class Session:
    console_selection_info: MAConsoleSelectionInfo | None = None
    layers_names: list[str] = field(default_factory=list)
    fixtures: list[MAFixture] = field(default_factory=list)
    repatch_items: list[RepatchInfo] = field(default_factory=list)

    def from_console(self) -> None:
        if self.console_selection_info is None:
            raise ValueError("Console selection info not set")

        self.layers_names = list()
        self.fixtures = list()
        self.repatch_items = list()

        with MAConsole(self.console_selection_info) as ma_console:
            layers = ma_console.list_layers()
            self.layers_names = list(layers.values())

            universes = list()
            for layer_id, layer_name in layers.items():
                for fixture in ma_console.list_fixtures(layer_id=layer_id):
                    if fixture.universe not in universes:
                        universes.append(fixture.universe)

                    self.fixtures.append(fixture)

            self.fixtures.sort(key=lambda f: f.id)

            for universe in sorted(universes):
                self.repatch_items.append(RepatchInfo(universe_source=universe, universe_target=universe))

    def repatch_console(self):
        if self.console_selection_info is None:
            raise ValueError("Console selection info not set")

        repatch_dict = {repatch.universe_source: repatch.universe_target for repatch in self.repatch_items}
        with MAConsole(self.console_selection_info) as ma_console:
            ma_console.clear_patch()
            for fixture in self.fixtures:
                target_universe = repatch_dict[fixture.universe]
                if target_universe is None:
                    continue

                target_patch = f"{target_universe}.{fixture.channel}"
                ma_console.set_fixture_patch(fixture.id, target_patch)

                _logger.info(f"Repatched {fixture.name} [{fixture.id}] to {target_patch}")

    def make_csv_patch(self, filename: str):
        repatch_dict = {repatch.universe_source: repatch.universe_target for repatch in self.repatch_items}
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Channel", "Patch"])
            for fixture in self.fixtures:
                target_universe = repatch_dict.get(fixture.universe)
                patch = f"{target_universe}.{fixture.channel}" if target_universe else ""
                writer.writerow([fixture.id, patch])
