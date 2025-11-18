from concurrent.futures import Future
import asyncio
import threading
import time

from pythonhelpers.cli import remove_color_and_style_special_chars

from telnetlib3 import TelnetReader, TelnetWriter, open_connection


class Telnet:
    def __init__(self, host: str, port: int, read_buffer_size: int, response_wait_time: float):
        self.host = host
        self.port = port
        self.response_wait_time = response_wait_time
        self.read_buffer_size = read_buffer_size
        self._reader: TelnetReader = None
        self._writer: TelnetWriter = None

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    @property
    def connected(self):
        return self._reader is not None and not self._reader.at_eof()

    def connect(self):
        self._reader, self._writer = self._run_coro(open_connection(self.host, self.port)).result()
        self._recv()
        if self._reader.at_eof():
            raise ConnectionError('Failed to connect')

    def disconnect(self):
        if self._reader is not None:
            self._writer.close()
            self._writer = None

            self._reader.feed_eof()
            self._reader = None

        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()

    def send(self, text: str) -> str:
        if not self._writer:
            raise ConnectionError('Not connected')

        self._writer.write(text)
        time.sleep(self.response_wait_time)  # FIXME: of course, do better
        return self._recv()

    def _recv(self) -> str:
        response = remove_color_and_style_special_chars(
            self._run_coro(self._reader.read(self.read_buffer_size)).result()
        )
        return response

    def __del__(self):
        self.disconnect()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _run_coro(self, coro) -> Future:
        return asyncio.run_coroutine_threadsafe(coro, self._loop)
