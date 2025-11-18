import time

import re
import logging

from grandma2telnet.lib.ma.exceptions import MARemoteException
from grandma2telnet.lib.ma.table_parser import TableParser
from grandma2telnet.lib.telnet import Telnet

_logger = logging.getLogger("LowLevelApi")
_RE_ERROR = re.compile(pattern=r'Error : (.+)', flags=re.MULTILINE)


class LowLevelApi:

    def __init__(self, host: str):
        self.host = host
        self._telnet = Telnet(
            host=self.host, port=30000,
            read_buffer_size=9000,
            response_wait_time=.1
        )

        self.drive_index = -1
        self.current_dest: str | None = None

    def connect(self):
        now = time.time()
        self._telnet.connect()
        if not self._telnet.connected:
            raise ConnectionError(f'Could not connect to {self.host}')

        _logger.info(f"Connected to {self.host} in {time.time() - now:.2f}s")

    def disconnect(self):
        self._telnet.disconnect()
        _logger.info(f"Disconnected from {self.host}")

    def login(self, username: str, password: str | None = None) -> None:
        if password is None:
            self._send(f'Login "{username}"\r')
        else:
            self._send(f'Login "{username}" "{password}"\r')

        _logger.info(f"Logged in as {username}")

    def set_drive(self, drive_index: int) -> None:
        if self.drive_index != drive_index:
            self.drive_index = drive_index
            self._send(f'sd {self.drive_index}\r')

    def change_dest(self, destination: str) -> None:
        self.current_dest = destination
        self._send('cd /\r')

        if self.current_dest == "/":
            return

        for path_item in destination.split('/'):
            try:
                self._send(f'cd {path_item}\r')
            except MARemoteException:
                self.current_dest = None
                raise MARemoteException(f"Could not change destination to '{destination}', please check console") from None

    def import_(self, item: str, position: int = None) -> None:
        if position is None:
            self._send(f'import "{item}"\r')
        else:
            self._send(f'import "{item}" At {position}\r')

    def clear_all(self):
        self._send('clearall\r')

    def set_fixture_type(self, fixture_type_id: int, fixture_first: int, fixture_last: int | None = None):
        if fixture_last is None:
            self._send(f'Assign FixtureType {fixture_type_id} At {fixture_first}\r')
        else:
            self._send(f'Assign FixtureType {fixture_type_id} At {fixture_first} Thru {fixture_last}\r')

    def list_and_parse_table(self) -> TableParser:
        stream_lines = self.list().split('\n\r')
        return TableParser(stream_lines[1:-1])

    def list(self):
        return self._send('List\r')

    def delete(self, first: int, last: int | None):
        if last is None:
            self._send(f"Delete {first} /nc\r")
            return

        self._send(f"Delete {first} Thru {last} /nc\r")

    def _send(self, command: str) -> str:
        _logger.debug(f"Sending command: {command}")
        response = self._telnet.send(command)
        
        error = _RE_ERROR.findall(response)
        if error:
            raise MARemoteException(error[0])
        
        return response
