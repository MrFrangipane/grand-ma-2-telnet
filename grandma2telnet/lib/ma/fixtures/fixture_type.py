from dataclasses import dataclass


@dataclass
class FixtureType:
    manufacturer: str
    name: str
    mode: str
