from dataclasses import dataclass, field

from grandma2telnet.lib.ma.fixtures.fixture import FixtureType


@dataclass
class FixtureLibrary:
    version: str
    fixtures: list[FixtureType] = field(default_factory=list)
