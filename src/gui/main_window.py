import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QAction, QMenuBar, QApplication
from PyQt5.QtCore import Qt
from gui.desktop_files import Desktop as FilesDesktop
from gui.desktop_player import MediaPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Симулятор Windows 98')
        self.setGeometry(300, 300, 1600, 600)

        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        self.filesPanel = self.createFilesPanel()
        self.playerPanel = self.createPlayerPanel()

        self.splitter.addWidget(self.filesPanel)
        self.splitter.addWidget(self.playerPanel)

        self.splitter.setSizes([800, 800])

        menubar = self.menuBar()
        viewMenu = menubar.addMenu('View')

        self.toggleFilesAction = QAction('Show Files Panel', self, checkable=True, checked=True)
        self.toggleFilesAction.triggered.connect(self.toggleFilesPanel)
        viewMenu.addAction(self.toggleFilesAction)

        self.togglePlayerAction = QAction('Show Media Player', self, checkable=True, checked=True)
        self.togglePlayerAction.triggered.connect(self.togglePlayerPanel)
        viewMenu.addAction(self.togglePlayerAction)

    def createFilesPanel(self):
        panel = QWidget()
        panelLayout = QVBoxLayout(panel)
        panel.setStyleSheet("border: 2px solid blue;")

        desktop = FilesDesktop(panel)
        desktop.setStyleSheet("background-color: lightblue;")
        panelLayout.addWidget(desktop)

        return panel

    def createPlayerPanel(self):
        panel = QWidget()
        panelLayout = QVBoxLayout(panel)
        panel.setStyleSheet("border: 2px solid green;")

        player = MediaPlayer()
        player.setStyleSheet("background-color: lightgreen;")
        panelLayout.addWidget(player)

        return panel

    def toggleFilesPanel(self):
        self.filesPanel.setVisible(self.toggleFilesAction.isChecked())

    def togglePlayerPanel(self):
        self.playerPanel.setVisible(self.togglePlayerAction.isChecked())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
