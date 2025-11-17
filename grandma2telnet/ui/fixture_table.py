from PySide6.QtWidgets import QGroupBox, QGridLayout, QTableWidget, QPushButton, QTableWidgetItem

from pyside6helpers import icons

from grandma2telnet.ui.components import Components


class FixtureTableWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layer_index = None

        self.setTitle("Fixtures")

        layout = QGridLayout(self)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.refresh = QPushButton()
        self.refresh.setIcon(icons.refresh())
        self.refresh.setToolTip("Refresh list of fixtures")
        self.refresh.clicked.connect(self._refresh)
        layout.addWidget(self.refresh)

    def set_layer(self, layer_index: int):
        self._layer_index = layer_index
        self._refresh()

    def _refresh(self):
        if self._layer_index is None:
            return

        Components().main_window.set_wait(True)
        ma_console = Components().ma_console

        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(['Name', 'ID', 'Universe', 'Channel'])

        for row, fixture in enumerate(ma_console.list_fixtures(self._layer_index)):
            self.table.setRowCount(row + 1)
            self.table.setItem(row, 0, QTableWidgetItem(str(fixture.name)))
            self.table.setItem(row, 1, QTableWidgetItem(str(fixture.id)))
            self.table.setItem(row, 2, QTableWidgetItem(str(fixture.universe)))
            self.table.setItem(row, 3, QTableWidgetItem(str(fixture.channel)))

        Components().main_window.set_wait(False)
