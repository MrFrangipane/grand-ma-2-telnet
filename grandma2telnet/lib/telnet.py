import time

import telnetlib3
import asyncio

from pythonhelpers.cli import remove_color_and_style_special_chars


class Telnet:
    def __init__(self, host: str, port: int, read_buffer_size: int, response_wait_time: float):
        self.host = host
        self.port = port
        self.response_wait_time = response_wait_time
        self.read_buffer_size = read_buffer_size
        self._reader: telnetlib3.TelnetReader = None
        self._writer: telnetlib3.TelnetWriter = None

    def __del__(self):
        self.disconnect()

    @property
    def connected(self):
        return self._reader is not None and not self._reader.at_eof()

    def connect(self) -> None:
        loop = asyncio.get_event_loop()
        self._reader, self._writer = loop.run_until_complete(telnetlib3.open_connection(self.host, self.port))
        self._recv()
        if self._reader.at_eof():
            raise ConnectionError('Failed to connect')

    def disconnect(self) -> None:
        if self._reader is not None:
            self._writer.close()
            self._writer = None

            self._reader.feed_eof()
            self._reader = None

    def send(self, text: str) -> str:
        if not self._writer:
            raise ConnectionError('Not connected')

        self._writer.write(text)
        time.sleep(self.response_wait_time)  # FIXME: of course, do better
        return self._recv()

    def _recv(self) -> str:
        loop = asyncio.get_event_loop()
        response = remove_color_and_style_special_chars(loop.run_until_complete(
            self._reader.read(self.read_buffer_size))
        )
        return response
