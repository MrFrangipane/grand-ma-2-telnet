from dataclasses import dataclass, field

from grandma2telnet.lib.ma.fixtures.fixture import Fixture


@dataclass
class FixtureLibrary:
    version: str
    fixtures: list[Fixture] = field(default_factory=list)
