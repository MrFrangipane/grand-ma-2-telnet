import logging

from PySide6.QtWidgets import QApplication

from pyside6helpers.main_window import MainWindow
from pyside6helpers import css, resources

from grandma2telnet.lib.session import SessionStore
from grandma2telnet.ui.central_widget import CentralWidget
from grandma2telnet.ui.components import Components


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    Components().session = SessionStore().new()

    app = QApplication()
    app.setApplicationName("GrandMA2 Telnet")
    app.setOrganizationName("Frangitron")
    css.load_onto(app)

    window = MainWindow(
        logo_filepath=resources.find(resource_name='frangitron-logo.png')
    )
    Components().main_window = window
    window.setCentralWidget(CentralWidget())
    window.show()

    app.exec()
