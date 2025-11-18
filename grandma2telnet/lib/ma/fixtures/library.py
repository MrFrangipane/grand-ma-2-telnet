from dataclasses import dataclass, field

from grandma2telnet.lib.ma.fixtures.fixture import MAFixtureType


@dataclass
class FixtureLibrary:
    version: str
    fixtures: list[MAFixtureType] = field(default_factory=list)
