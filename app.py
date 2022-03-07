from Inventory import app
import sys
from PyQt5 import Qt
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QShortcut
from PyQt5.QtGui import QKeySequence
from threading import Timer
from PyQt5.Qt import QMessageBox

# Define function for QtWebEngine
def ui(location):
    qt_app = QApplication(sys.argv)
    web = QWebEngineView()
    screen = qt_app.primaryScreen()
    size = screen.size()
    web.setWindowTitle("Inventory")
    web.resize(size.width(), size.height())
    web.setZoomFactor(1.5)


    def emit_pdf(finished):
        web.page().printToPdf('item.pdf')
        web.page().pdfPrintingFinished.connect(
            lambda *args: print('finished:', args))

    # if(QUrl == "http://127.0.0.1:5000/add-item"):
    #     web.loadFinished.connect(emit_pdf)
    # if(QUrl== "http://127.0.0.1:5000/issuedto"):
    #     print(web.url().toString())
    #
    #     web.loadFinished.connect(emit_pdf)
    # if(QUrl == "http://127.0.0.1:5000/download"):
    #     print(web.url().toString())
    #     web.loadFinished.connect(emit_pdf)


    web.load(QUrl(location))


    web.show()

    # display "File downloaded" message in dailog
    #result = QMessageBox.question(web, 'TITLE', 'MESSAGE', QMessageBox.Yes | QMessageBox.No)
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    Timer(1, lambda: ui("http://127.0.0.1:5000/")).start()
    app.run(debug=False)