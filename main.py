import sys

from PySide6.QtWidgets import QApplication

from interface.home import LiblitzHome


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LiblitzHome()
    window.show()

    sys.exit(app.exec())
