from dataclasses import dataclass

from pythonhelpers.vector import Vector3

from grandma2telnet.lib.ma.fixtures.fixture_type import FixtureType


@dataclass
class Fixture:
    id: int | None
    name: str
    type: FixtureType

    universe: int | None
    channel: int | None

    position: Vector3
    rotation: Vector3
