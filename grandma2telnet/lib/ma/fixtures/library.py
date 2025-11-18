from dataclasses import dataclass, field

from grandma2telnet.lib.ma.fixtures.fixture import MAFixtureType


@dataclass
class MAFixtureLibrary:
    version: str
    fixtures: list[MAFixtureType] = field(default_factory=list)
