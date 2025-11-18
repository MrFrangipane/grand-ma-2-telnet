import logging
import os

from grandma2telnet.lib.ma.installation import MAInstallation


_logger = logging.getLogger("InstallationStore")


class MAInstallationStore:
    def __init__(self):
        self.installations: dict[str, MAInstallation] = dict()

    def list_installations(self) -> list[MAInstallation]:
        self.installations = dict()

        root_installation_path = os.path.expandvars("%PROGRAMDATA%\\MA Lighting Technologies\\grandma")
        if not os.path.exists(root_installation_path):
            raise FileNotFoundError(f"Installation path {root_installation_path} does not exist")

        for item in sorted(os.listdir(root_installation_path)):
            fullpath = os.path.join(root_installation_path, item)
            if os.path.isdir(fullpath) and item.startswith("gma2_"):
                version = item.split("_")[-1]
                self.installations[version] = MAInstallation(
                    version=version,
                    fullpath=os.path.abspath(fullpath)
                )

        if not self.installations:
            _logger.warning("No installations found")
        else:
            _logger.info(f"Found installations: {', '.join(self.installations.keys())}")

        return list(self.installations.values())
