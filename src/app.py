import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStatusBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setWindowTitle('Windows 98 Simulator')
        self.setGeometry(300, 300, 600, 400)
        button = QPushButton('Click me', self)
        button.move(50, 50)
        button.clicked.connect(self.on_click)

    def on_click(self):
        self.statusBar().showMessage('Button clicked')

def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
