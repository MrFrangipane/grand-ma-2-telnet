from dataclasses import dataclass

from pythonhelpers.vector import Vector3

from grandma2telnet.lib.ma.fixtures.fixture_type import FixtureType


@dataclass
class Fixture:
    id: int
    name: str
    type: FixtureType

    universe: int
    channel: int

    position: Vector3
    rotation: Vector3
