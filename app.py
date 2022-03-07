from Inventory import app
import sys
from PyQt5 import Qt
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
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
    # def emit_pdf(file):
    #     web.page().printToPdf(file)
    #     web.page().pdfPrintingFinished.connect(
    #         lambda *args: print('finished:', args))
    #
    # if(web.url().toString() == "http://127.0.0.1:5000/add-item"):
    #
    #
    #     web.loadFinished.connect(emit_pdf(file="item.pdf"))
    # if(web.url().toString() == "http://127.0.0.1:5000/issuedto"):
    #     print(web.url().toString(), file=sys.stderr)
    #
    #     web.loadFinished.connect(emit_pdf(file="issued-item.pdf"))
    # if(web.url().toString() == "http://127.0.0.1:5000/main-ledger"):
    #     print(web.url().toString(), file=sys.stderr)
    #
    #     web.loadFinished.connect(emit_pdf(file="ledger.pdf"))


    web.load(QUrl(location))
    print(web.url().toString(), file=sys.stderr)
    web.show()

    # display "File downloaded" message in dailog
    #result = QMessageBox.question(web, 'TITLE', 'MESSAGE', QMessageBox.Yes | QMessageBox.No)
    sys.exit(qt_app.exec_())


if __name__ == '__main__':
    Timer(1, lambda: ui("http://127.0.0.1:5000/")).start()
    app.run(debug=False)