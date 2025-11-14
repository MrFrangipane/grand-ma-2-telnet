from grandma2telnet.lib.ma.low_level_api import LowLevelApi


class MA:

    def __init__(self, host: str):
        self._low_level_api = LowLevelApi(host=host)

    def connect(self, username: str, password: str):
        self._low_level_api.connect()
        self._low_level_api.login(username, password)

    def add_fixture_type(self, fixture_type_name: str):
        self._low_level_api.set_drive(1)
        self._low_level_api.change_dest('EditSetup/FixtureTypes')
        self._low_level_api.import_(fixture_type_name)
