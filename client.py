#-*- coding: UTF-8 -*-
#/usr/bin/env python3

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QUrl
from PyQt5.QtWidgets import (QAction, QApplication, QLineEdit, QMainWindow,
        QSizePolicy, QStyle, QTextEdit)
from PyQt5.QtNetwork import QNetworkProxyFactory, QNetworkRequest
from PyQt5.QtWebKitWidgets import QWebPage, QWebInspector, QWebView

#import jquery_rc

class MainWindow(QMainWindow):
    def __init__(self, url):
        super(MainWindow, self).__init__()

        self.progress = 0
        
        fd = QFile(":/views/static/js/brython.js")

        if fd.open(QIODevice.ReadOnly | QFile.Text):
            self.Bryton = QTextStream(fd).readAll()
            fd.close()
        else:
            self.Brython= ''
        
        QNetworkProxyFactory.setUseSystemConfiguration(True)

        self.view = QWebView(self)
        self.view.load(url)
        self.view.loadFinished.connect(self.adjustLocation)
        self.view.titleChanged.connect(self.adjustTitle)
        self.view.loadProgress.connect(self.setProgress)
        self.view.loadFinished.connect(self.finishLoading)
        self.inspector = QWebInspector()
        self.inspector.setPage(self.view.page())
        
        toolBar = self.addToolBar("Navigation")
        toolBar.addAction(self.view.pageAction(QWebPage.Back))
        toolBar.addAction(self.view.pageAction(QWebPage.Forward))
        toolBar.addAction(self.view.pageAction(QWebPage.Reload))
        toolBar.addAction(self.view.pageAction(QWebPage.Stop))
        
        self.setCentralWidget(self.view)
        
    def viewSource(self):
        accessManager = self.view.page().networkAccessManager()
        request = QNetworkRequest(self.view.url())
        reply = accessManager.get(request)
        reply.finished.connect(self.slotSourceDownloaded)

    def slotSourceDownloaded(self):
        reply = self.sender()
        self.textEdit = QTextEdit()
        self.textEdit.setAttribute(Qt.WA_DeleteOnClose)
        self.textEdit.show()
        self.textEdit.setPlainText(QTextStream(reply).readAll())
        self.textEdit.resize(600, 400)
        reply.deleteLater()

    def adjustLocation(self):
        #self.locationEdit.setText(self.view.url().toString())
        print("Change url")
        print(self.view.url().toString())
        #elf.view.load(self.view.url())
    def changeLocation(self):
        #url = QUrl.fromUserInput(self.locationEdit.text())
        self.view.load(url)
        self.view.setFocus()

    def adjustTitle(self):
        if 0 < self.progress < 100:
            self.setWindowTitle("%s (%s%%)" % (self.view.title(), self.progress))
        else:
            self.setWindowTitle(self.view.title())

    def setProgress(self, p):
        self.progress = p
        self.adjustTitle()

    def finishLoading(self):
        self.progress = 100
        self.adjustTitle()
        self.view.page().mainFrame().evaluateJavaScript(self.Brython)
        

    def highlightAllLinks(self):
        code = """$('a').each(
                    function () {
                        $(this).css('background-color', 'yellow') 
                    } 
                  )"""
        self.view.page().mainFrame().evaluateJavaScript(code)

    def rotateImages(self, invert):
        if invert:
            code = """
                $('img').each(
                    function () {
                        $(this).css('-webkit-transition', '-webkit-transform 2s'); 
                        $(this).css('-webkit-transform', 'rotate(180deg)') 
                    } 
                )"""
        else:
            code = """
                $('img').each(
                    function () { 
                        $(this).css('-webkit-transition', '-webkit-transform 2s'); 
                        $(this).css('-webkit-transform', 'rotate(0deg)') 
                    } 
                )"""

        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeGifImages(self):
        code = "$('[src*=gif]').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeInlineFrames(self):
        code = "$('iframe').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeObjectElements(self):
        code = "$('object').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)

    def removeEmbeddedElements(self):
        code = "$('embed').remove()"
        self.view.page().mainFrame().evaluateJavaScript(code)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        url = QUrl(sys.argv[1])
    else:
        url = QUrl('http://localhost:8000')

    browser = MainWindow(url)
    browser.show()

sys.exit(app.exec_())
