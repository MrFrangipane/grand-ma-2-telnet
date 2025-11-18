from PySide6.QtWidgets import QGroupBox, QGridLayout, QTableWidget, QPushButton, QTableWidgetItem, QAbstractItemView

from pyside6helpers import icons

from grandma2telnet.lib import MAConsole
from grandma2telnet.ui.components import Components


class FixtureTableWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layer_index = None
        self._block_signals = False
        self._fixture_cache = dict()
        self._propagating_edit = False

        self.setTitle("Fixtures")

        layout = QGridLayout(self)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.SelectedClicked |
            QAbstractItemView.EditKeyPressed |
            QAbstractItemView.AnyKeyPressed
        )
        self.table.itemChanged.connect(self._on_item_changed)
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

        self._fixture_cache = dict()

        self._block_signals = True
        Components().main_window.set_wait(True)

        labels = ['Name', 'ID', 'Type', 'Universe', 'Channel']
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(len(labels))
        self.table.setHorizontalHeaderLabels(labels)

        with MAConsole(Components().console_selection_info) as ma_console:
            for row, fixture in enumerate(ma_console.list_fixtures(self._layer_index)):
                self._fixture_cache[row] = fixture

                self.table.setRowCount(row + 1)
                self.table.setItem(row, 0, QTableWidgetItem(str(fixture.name)))
                self.table.setItem(row, 1, QTableWidgetItem(str(fixture.id)))
                self.table.setItem(row, 2, QTableWidgetItem(str(fixture.type)))
                self.table.setItem(row, 3, QTableWidgetItem(str(fixture.universe)))
                self.table.setItem(row, 4, QTableWidgetItem(str(fixture.channel)))

        Components().main_window.set_wait(False)
        self._block_signals = False

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._block_signals or self._propagating_edit:
            return

        table = self.table
        selected_items = table.selectedItems()
        col = item.column()
        new_value = item.text()

        same_column_items = [i for i in selected_items if i.column() == col]
        self._propagating_edit = True

        for i in same_column_items:
            row = i.row()
            print(self._fixture_cache[row])

            if i is item:
                continue
            i.setText(new_value)

        self._propagating_edit = False
