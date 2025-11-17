from PySide6.QtWidgets import QGroupBox, QListWidget, QGridLayout, QPushButton

from grandma2telnet.lib.ma.exceptions import MARemoteException
from pyside6helpers import icons

from grandma2telnet.ui.components import Components


class LayerListWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._block_signals = False

        self.setTitle("Layers")

        layout = QGridLayout(self)

        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        self.list.currentItemChanged.connect(self._on_layer_selected)
        layout.addWidget(self.list)

        self.refresh = QPushButton()
        self.refresh.setIcon(icons.refresh())
        self.refresh.setToolTip("Refresh list of layers")
        self.refresh.clicked.connect(self._refresh)
        layout.addWidget(self.refresh)

    def _refresh(self):
        self._block_signals = True
        Components().main_window.set_wait(True)

        ma_console = Components().ma_console
        if not ma_console.is_connected:
            try:
                ma_console.connect()
            except MARemoteException:
                self._block_signals = False
                return

        layers = ma_console.list_layers()
        self.list.clear()
        self.list.addItems(list(layers.values()))

        Components().main_window.set_wait(False)
        self._block_signals = False

    def _on_layer_selected(self, index):
        if self._block_signals:
            return

        Components().fixture_table.set_layer(self.list.currentIndex().row() + 1)
