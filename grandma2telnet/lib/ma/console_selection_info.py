from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class MAConsoleSelectionInfo:
    host: str
    password: str
    username: str
    version: str | None = None
