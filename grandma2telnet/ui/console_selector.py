from PySide6.QtWidgets import QComboBox, QFormLayout, QLineEdit, QGroupBox, QPushButton

from pyside6helpers import icons

from grandma2telnet.ui.components import Components


class ConsoleSelectorWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._block_signals = False

        self.setTitle("Console Selector")

        layout = QFormLayout(self)

        self.host = QLineEdit("127.0.0.1")
        self.host.textChanged.connect(self._login_changed)
        layout.addRow("Host", self.host)

        self.username = QLineEdit("Administrator")
        self.username.textChanged.connect(self._login_changed)
        layout.addRow("Username", self.username)

        self.password = QLineEdit("admin")
        self.password.textChanged.connect(self._login_changed)
        layout.addRow("Password", self.password)

        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self._installation_changed)
        layout.addRow("Installation", self.combo)

        self.refresh = QPushButton()
        self.refresh.setIcon(icons.refresh())
        self.refresh.setToolTip("Refresh list of installations")
        self.refresh.clicked.connect(self._refresh)
        layout.addWidget(self.refresh)

        self._refresh()

    def _refresh(self):
        Components().main_window.set_wait(True)
        self._block_signals = True
        self.combo.clear()
        self.combo.addItems(Components().ma_console.installations)
        self._block_signals = False

        if Components().ma_console.installations:
            self.combo.setCurrentIndex(self.combo.count() - 1)
            self._installation_changed(self.combo.currentIndex())

        self._login_changed()
        Components().main_window.set_wait(False)

    def _installation_changed(self, index):
        if self._block_signals:
            return

        ma_console = Components().ma_console
        ma_console.set_installation(version=self.combo.currentText())

    def _login_changed(self):
        if self._block_signals:
            return

        ma_console = Components().ma_console
        ma_console.host = self.host.text()
        ma_console.username = self.username.text()
        ma_console.password = self.password.text()
