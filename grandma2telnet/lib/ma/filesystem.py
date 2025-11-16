import os

from grandma2telnet.lib.ma.installation import Installation


class FileSystem:
    def __init__(self):
        self.installations: dict[str, Installation] = dict()

    def list_installations(self) -> list[Installation]:
        self.installations = dict()

        root_installation_path = os.path.expandvars("%PROGRAMDATA%\\MA Lighting Technologies\\grandma")
        if not os.path.exists(root_installation_path):
            raise FileNotFoundError(f"Installation path {root_installation_path} does not exist")

        for item in sorted(os.listdir(root_installation_path)):
            fullpath = os.path.join(root_installation_path, item)
            if os.path.isdir(fullpath) and item.startswith("gma2_"):
                version = item.split("_")[-1]
                self.installations[version] = Installation(
                    version=version,
                    fullpath=os.path.abspath(fullpath)
                )

        return list(self.installations.values())
