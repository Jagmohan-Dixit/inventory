from Inventory import app
import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from threading import Timer


# Define function for QtWebEngine
def ui(location):
    qt_app = QApplication(sys.argv)
    web = QWebEngineView()
    screen = qt_app.primaryScreen()
    size = screen.size()
    web.setWindowTitle("Inventory")
    web.resize(size.width(), size.height())
    web.setZoomFactor(1.5)
    web.load(QUrl(location))
    web.show()
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    Timer(1, lambda: ui("http://127.0.0.1:5000/")).start()
    app.run(debug=False)