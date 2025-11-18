from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RepatchInfo:
    universe_source: int
    universe_target: int | None

