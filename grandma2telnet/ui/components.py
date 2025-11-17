from dataclasses import dataclass

from pyside6helpers.main_window import MainWindow
from pythonhelpers.singleton_metaclass import SingletonMetaclass

from grandma2telnet.lib import MA


@dataclass
class Components(metaclass=SingletonMetaclass):
    fixture_table = None  # FIXME make an AbstractFixtureTableWidget
    ma_console = MA()
    main_window: MainWindow | None = None
