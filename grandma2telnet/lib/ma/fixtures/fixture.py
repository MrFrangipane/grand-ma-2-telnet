from dataclasses import dataclass

from dataclasses_json import dataclass_json

from grandma2telnet.lib.ma.fixtures.fixture_type import MAFixtureType


@dataclass_json
@dataclass
class MAFixture:
    id: int | None
    name: str
    type: str  # TODO use MAFixtureType

    layer_id: int

    universe: int | None
    channel: int | None
