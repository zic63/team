import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMenu, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()  # Инициализация пользовательского интерфейса

    def initUI(self):
        self.setWindowTitle('Симулятор Windows 98')  # Устанавливаем заголовок окна
        self.setGeometry(300, 300, 800, 600)  # Задаем размеры и положение окна

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)  # Основной макет окна

        self.setupDesktop()  # Настраиваем рабочий стол
        self.setupTaskbar()  # Настраиваем панель задач

    def setupTaskbar(self):
        # Настройка панели задач
        self.taskbar = QWidget(self)
        self.taskbar.setFixedHeight(40)  # Фиксируем высоту панели задач
        self.taskbar.setStyleSheet("background-color: grey")  # Устанавливаем цвет панели задач

        self.startBtn = QPushButton('Пуск', self.taskbar)
        self.startBtn.setFixedSize(100, 30)  # Фиксируем размер кнопки "Пуск"
        self.startBtn.clicked.connect(self.showStartMenu)  # Подключаем кнопку к методу открытия меню "Пуск"

        hbox = QHBoxLayout(self.taskbar)
        hbox.addWidget(self.startBtn)  # Добавляем кнопку "Пуск" на панель задач
        hbox.addStretch(1)  # Заполняем оставшееся пространство
        hbox.setContentsMargins(5, 5, 5, 5)  # Устанавливаем отступы внутри панели задач

        self.mainLayout.addWidget(self.taskbar)  # Добавляем панель задач в основной макет

        self.startMenu = QMenu(self)
        self.startMenu.addAction('Создать иконку', self.createIcon)  # Добавляем пункт меню "Создать иконку"
        self.startMenu.addAction('Создать папку', self.createFolder)  # Добавляем пункт меню "Создать папку"

    def showStartMenu(self):
        # Метод для отображения меню "Пуск"
        self.startMenu.exec_(self.startBtn.mapToGlobal(self.startBtn.rect().bottomLeft()))

    def createIcon(self):
        # Метод для создания новой иконки на рабочем столе
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите файл для создания иконки", "", "Все файлы (*)")
        if fileName:
            iconName = os.path.basename(fileName)
            self.desktop.createDesktopIcon(iconName, fileName)

    def createFolder(self):
        # Метод для создания новой папки на рабочем столе
        folderName, ok = QInputDialog.getText(self, 'Создать папку', 'Введите имя папки:')
        if ok and folderName:
            self.desktop.createDesktopFolder(folderName)

    def setupDesktop(self):
        # Настройка рабочего стола
        from gui.desktop import Desktop
        self.desktop = Desktop(self)
        self.mainLayout.addWidget(self.desktop)  # Добавляем рабочий стол в основной макет

    def closeEvent(self, event):
        # Сохраняем состояние иконок при закрытии приложения
        self.desktop.saveDesktopState()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
