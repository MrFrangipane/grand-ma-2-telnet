import os
from dataclasses import dataclass


@dataclass
class Installation:
    version: str
    fullpath: str

    @property
    def library(self):
        return os.path.join(self.fullpath, "library")

    @property
    def fixtures(self):
        return os.path.join(self.fullpath, "fixtures")

    @property
    def fixture_layers(self):
        return os.path.join(self.fullpath, "fixture_layers")

    @property
    def import_export(self):
        return os.path.join(self.fullpath, "importexport")
