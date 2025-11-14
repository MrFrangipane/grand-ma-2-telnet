from PySide6.QtWidgets import QApplication

from pyside6helpers.main_window import MainWindow

from grandma2telnet.ui.central_widget import CentralWidget


if __name__ == '__main__':
    app = QApplication()

    window = MainWindow()
    window.setCentralWidget(CentralWidget())
    window.show()

    app.exec()
