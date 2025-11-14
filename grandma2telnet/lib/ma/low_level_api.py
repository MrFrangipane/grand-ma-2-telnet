import re
import logging

from grandma2telnet.lib.telnet import Telnet
from grandma2telnet.lib.ma.exceptions import MARemoteException

_logger = logging.getLogger(__name__)
_RE_ERROR = re.compile(pattern=r'Error : (.+)', flags=re.MULTILINE)


class LowLevelApi:

    def __init__(self, host: str):
        self.host = host
        self._telnet = Telnet(
            host=self.host, port=30000,
            read_buffer_size=2048,
            response_wait_time=.01
        )

        self.drive_index = -1
        self.current_dest = ""

    def connect(self):
        self._telnet.connect()
        if not self._telnet.connected:
            raise ConnectionError(f'Could not connect to {self.host}')

        _logger.info(f"Connected to {self.host}")

    def login(self, username: str, password: str | None = None) -> None:
        if password is None:
            response = self._telnet.send(f'Login "{username}"\r')
        else:
            response = self._telnet.send(f'Login "{username}" "{password}"\r')

        error = _RE_ERROR.findall(response)
        if error:
            raise MARemoteException(error[0])

        _logger.info(f"Logged in as {username}")

    def set_drive(self, drive_index: int) -> None:
        if self.drive_index != drive_index:
            self.drive_index = drive_index
            self._telnet.send(f'sd {self.drive_index}\r')

    def change_dest(self, destination: str) -> None:
        # TODO: could minimize telnet calls by navigating intelligently
        if self.current_dest != destination:
            self.current_dest = destination
            self._telnet.send('cd /\r')
            for path_item in destination.split('/'):
                self._telnet.send(f'cd {path_item}\r')

    def import_(self, item: str, position: int = None) -> None:
        if position is None:
            self._telnet.send(f'import "{item}"\r')
        else:
            self._telnet.send(f'import "{item}" At {position}\r')
