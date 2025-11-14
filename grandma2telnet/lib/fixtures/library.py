from dataclasses import dataclass, field

from grandma2telnet.lib.fixtures.fixture import Fixture


@dataclass
class Library:
    version: str
    fullpath: str
    fixtures: list[Fixture] = field(default_factory=list)
