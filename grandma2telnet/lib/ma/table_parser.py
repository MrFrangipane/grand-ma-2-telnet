from dataclasses import dataclass


class TableParser:

    @dataclass
    class _Header:
        name: str
        position_start: int
        position_end: int

    def __init__(self, stream_lines: list[str]):
        self._stream_lines = stream_lines
        if not self._stream_lines:
            raise ValueError("Stream is empty")

        self._headers = self._parse_headers()
        self.lines = self._parse_lines()

    @property
    def headers(self) -> list[str]:
        return [header.name for header in self._headers]

    def _parse_headers(self) -> list[_Header]:
        head = self._stream_lines[0]
        items = head.split()
        headers = list()

        reading_position = 0
        for index, item in enumerate(items):
            next_index = index + 1
            end_position = head.index(items[next_index]) if next_index < len(items) else len(head)
            headers.append(TableParser._Header(
                name=item,
                position_start=reading_position,
                position_end=end_position
            ))
            reading_position = end_position

        return headers

    def _parse_lines(self) -> list[dict[str, str]]:
        lines = list()

        if not self._headers:
            raise ValueError("Headers not parsed yet")

        for line in self._stream_lines[1:]:
            lines.append({header.name: line[header.position_start:header.position_end].strip() for header in self._headers})

        return lines


if __name__ == "__main__":
    from pprint import pprint

    RESPONSE = """
           Name                           FixId  ChaId  FixtureType                       Patch   NoParameters  PosX  PosY  PosZ  RotX  RotY  RotZ  Info  RDMID  
Fixture 33 BeamZ Nereid380B Standard 1.2  33     -      3 Nereid380B Outdoor 18 Channels   1.279  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 34 BeamZ Nereid380B Standard 1.2  34     -      3 Nereid380B Outdoor 18 Channels   1.297  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 35 BeamZ Nereid380B Standard 1.2  35     -      3 Nereid380B Outdoor 18 Channels   1.315  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 36 BeamZ Nereid380B Standard 1.2  36     -      3 Nereid380B Outdoor 18 Channels   1.333  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 37 BeamZ Nereid380B Standard 1.2  37     -      3 Nereid380B Outdoor 18 Channels   1.351  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 38 BeamZ Nereid380B Standard 1.2  38     -      3 Nereid380B Outdoor 18 Channels   1.369  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 39 BeamZ Nereid380B Standard 1.2  39     -      3 Nereid380B Outdoor 18 Channels   1.387  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 40 BeamZ Nereid380B Standard 1.2  40     -      3 Nereid380B Outdoor 18 Channels   1.405  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 41 BeamZ Nereid380B Standard 1.2  41     -      3 Nereid380B Outdoor 18 Channels   1.423  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 42 BeamZ Nereid380B Standard 1.2  42     -      3 Nereid380B Outdoor 18 Channels   1.441  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 43 BeamZ Nereid380B Standard 1.2  43     -      3 Nereid380B Outdoor 18 Channels   1.459  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)
Fixture 44 BeamZ Nereid380B Standard 1.2  44     -      3 Nereid380B Outdoor 18 Channels   1.477  No            0.00  0.00  0.00  0.00  0.00  0.00                (1)"""

    table_parser = TableParser(RESPONSE.splitlines()[1:])
    pprint(table_parser.headers)
    pprint(table_parser.lines)
