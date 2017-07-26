import sys
import Stereo
import functools
from PyQt4 import QtCore, QtGui


class Gui(QtGui.QWidget):
    def __init__(self):
        super(Gui, self).__init__()
        self.timer = []
        self._initGui()
        self._addMenu()
        self._addTestMenu()

    def _addTestMenu(self):
        Test = self.menu.addMenu('Test')
        openAction = QtGui.QAction('Show Stereo Images', self)
        openAction.triggered.connect(functools.partial(Stereo.ShowStereo, obj = self))
        
        disparityAction = QtGui.QAction('Calculate Disparity', self)
        disparityAction.triggered.connect(functools.partial(Stereo.ShowDisparity, obj = self))

        Test.addAction(openAction)
        Test.addAction(disparityAction)

    def _initGui(self):
        screenShape = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screenShape.width(), screenShape.height())
        self.setWindowTitle('App')

    def _addMenu(self):
        exitAction = QtGui.QAction('Close', self)
        exitAction.triggered.connect(QtGui.qApp.exit)
        openfileAction = QtGui.QAction('Open', self)
        openfileAction.triggered.connect(self.getOpenFileNames)
        screenshotAction = QtGui.QAction('Screenshot', self)
        screenshotAction.triggered.connect(self.saveScreenshot)

        self.menu = QtGui.QMenuBar(self)
        File = self.menu.addMenu('File')
        File.addAction(openfileAction)
        File.addAction(screenshotAction)
        File.addAction(exitAction)

    def saveScreenshot(self):
        savefile = self.getSaveFileName()
        pix = QtGui.QPixmap.grabWidget(self)
        pix.save(savefile)

    def getOpenFileNames(self):
        openfile = QtGui.QFileDialog.getOpenFileNames(self)
        openfile = [str(x) for x in openfile]
        return openfile
    
    def getSaveFileName(self):
        savefile = QtGui.QFileDialog.getSaveFileName(self)
        return str(savefile)

    def clearLayout(self):
        layout = self.layout()
        for timer in self.timer:
            timer.stop()
        self.timer = []
        if layout is not None:
            QtGui.QWidget().setLayout(self.layout())


if __name__ == '__main__':
    app = QtGui.QApplication(['GG'])
    gui = Gui()
    gui.showFullScreen()
    sys.exit(app.exec_())
