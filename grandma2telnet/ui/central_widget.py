from PySide6.QtWidgets import QWidget, QGridLayout

from grandma2telnet.ui.components import Components
from grandma2telnet.ui.console_selector import ConsoleSelectorWidget
from grandma2telnet.ui.fixture_table import FixtureTableWidget
from grandma2telnet.ui.layer_list import LayerListWidget
from grandma2telnet.ui.session import SessionWidget


class CentralWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout(self)
        layout.addWidget(ConsoleSelectorWidget())
        layout.addWidget(LayerListWidget())

        Components().fixture_table = FixtureTableWidget()
        layout.addWidget(Components().fixture_table, 0, 1, 2, 1)

        layout.addWidget(SessionWidget(), 0, 2, 2, 1)

        layout.setColumnStretch(1, 50)
        layout.setColumnStretch(2, 50)
