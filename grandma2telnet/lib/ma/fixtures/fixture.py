from dataclasses import dataclass

from dataclasses_json import dataclass_json

from grandma2telnet.lib.ma.fixtures.fixture_type import MAFixtureType


@dataclass_json
@dataclass
class Fixture:
    id: int | None
    name: str
    type: MAFixtureType

    universe: int | None
    channel: int | None
