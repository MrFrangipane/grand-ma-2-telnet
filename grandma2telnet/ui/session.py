from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox, QGridLayout, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView

from pyside6helpers import message_box, icons

from grandma2telnet.lib.session import SessionStore
from grandma2telnet.ui.components import Components


class SessionWidget(QGroupBox):

    _filename = "session.json"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTitle("Session")

        layout = QGridLayout(self)

        self.button_from_console = QPushButton("Load from Console")
        self.button_from_console.setIcon(icons.download())
        self.button_from_console.clicked.connect(self._from_console)
        layout.addWidget(self.button_from_console)

        self.button_from_file = QPushButton("Load from File")
        self.button_from_file.setIcon(icons.file())
        self.button_from_file.clicked.connect(self._from_file)
        layout.addWidget(self.button_from_file)

        self.table_repatch = QTableWidget()
        self.table_repatch.setAlternatingRowColors(True)
        self.table_repatch.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.SelectedClicked |
            QAbstractItemView.EditKeyPressed |
            QAbstractItemView.AnyKeyPressed
        )
        self.table_repatch.itemChanged.connect(self._on_repatch_item_changed)
        layout.addWidget(self.table_repatch)

        self.button_repatch_console = QPushButton("Repatch console")
        self.button_repatch_console.setIcon(icons.upload())
        self.button_repatch_console.clicked.connect(self._repatch_console)
        layout.addWidget(self.button_repatch_console)

    def _from_console(self):
        if Components().session.fixtures:
            if not message_box.confirmation_box(["Session is not empty.", "Loading from console will overwrite layers and fixtures !"]):
                return

        Components().main_window.set_wait(True)

        Components().session.from_console()
        SessionStore().save(Components().session, self._filename)
        self._update_repatch_table()

        Components().main_window.set_wait(False)

    def _from_file(self):
        if Components().session.fixtures:
            if not message_box.confirmation_box(["Session is not empty.", "Loading from file will overwrite layers and fixtures !"]):
                return

        Components().main_window.set_wait(True)

        Components().session = SessionStore().load(self._filename)
        self._update_repatch_table()

        Components().main_window.set_wait(False)

    def _repatch_console(self):
        Components().main_window.set_wait(True)
        Components().session.repatch_console()
        Components().main_window.set_wait(False)

    def _update_repatch_table(self):
        labels = ['Source universe', 'Target universe']

        self.table_repatch.clear()
        self.table_repatch.setRowCount(len(Components().session.repatch_items))
        self.table_repatch.setColumnCount(len(labels))
        self.table_repatch.setHorizontalHeaderLabels(labels)

        for row, repatch_info in enumerate(Components().session.repatch_items):
            source_item = QTableWidgetItem(str(repatch_info.universe_source))
            source_item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
            self.table_repatch.setItem(row, 0, source_item)
            self.table_repatch.setItem(row, 1, QTableWidgetItem(str(repatch_info.universe_target)))

    def _on_repatch_item_changed(self, item: QTableWidgetItem):
        row = item.row()
        value = int(item.text()) if item.text() else None
        Components().session.repatch_items[row].universe_target = value
        SessionStore().save(Components().session, self._filename)
