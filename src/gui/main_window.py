from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QMenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupDesktop()  # Инициализация рабочего стола

    def initUI(self):
        self.setWindowTitle('Windows 98 Simulator')  # Установка заголовка окна
        self.setGeometry(300, 300, 800, 600)  # Установка размера и позиции окна
        self.setupTaskbar()  # Настройка панели задач

    def setupTaskbar(self):
        # Создание и настройка панели задач
        self.taskbar = QWidget(self)
        self.taskbar.setGeometry(0, self.height() - 40, self.width(), 40)
        self.taskbar.setStyleSheet("background-color: grey")
        self.setupStartMenu()  # Настройка кнопки "Пуск" и меню

    def setupStartMenu(self):
        # Кнопка "Пуск" и связанное меню
        self.startBtn = QPushButton('Пуск', self.taskbar)
        self.startBtn.move(10, 5)
        self.startBtn.clicked.connect(self.toggleStartMenu)
        self.startMenu = QMenuBar(self.taskbar)
        self.startMenu.hide()
        programs = self.startMenu.addMenu('Программы')
        programs.addAction('Блокнот')
        programs.addAction('Калькулятор')

    def setupDesktop(self):
        # Создание рабочего стола из класса Desktop
        from .desktop import Desktop
        self.desktop = Desktop(self)
        self.setCentralWidget(self.desktop)

    def toggleStartMenu(self):
        # Переключение видимости меню "Пуск"
        if self.startMenu.isVisible():
            self.startMenu.hide()
        else:
            self.startMenu.move(self.startBtn.x(), self.startBtn.y() + self.startBtn.height())
            self.startMenu.show()
