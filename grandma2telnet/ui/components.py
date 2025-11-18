from dataclasses import dataclass

from pyside6helpers.main_window import MainWindow
from pythonhelpers.singleton_metaclass import SingletonMetaclass

from grandma2telnet.lib import MAConsoleSelectionInfo


@dataclass
class Components(metaclass=SingletonMetaclass):
    console_selection_info: MAConsoleSelectionInfo | None = None
    fixture_table = None  # FIXME make an AbstractFixtureTableWidget
    main_window: MainWindow | None = None
