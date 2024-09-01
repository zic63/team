from PyQt5.QtWidgets import QWidget, QPushButton, QMenu
from PyQt5.QtCore import Qt

class DesktopIcon(QPushButton):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.setFixedSize(100, 50)  # Фиксированный размер иконки
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def openMenu(self, position):
        menu = QMenu()  # Создание контекстного меню
        menu.addAction('Открыть', self.open)
        menu.addAction('Переименовать', self.rename)
        menu.addAction('Удалить', self.delete)
        menu.exec_(self.mapToGlobal(position))

    def open(self):
        print(f"Открытие приложения {self.text()}...")  # Симуляция открытия приложения

    def rename(self):
        print("Функция переименования не реализована.")

    def delete(self):
        self.deleteLater()  # Удаление иконки с рабочего стола

class Desktop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupIcons()

    def setupIcons(self):
        # Создание иконок на рабочем столе
        self.notepadIcon = DesktopIcon("Блокнот", self)
        self.notepadIcon.move(100, 100)  # Расположение иконки Блокнота
        self.calculatorIcon = DesktopIcon("Калькулятор", self)
        self.calculatorIcon.move(100, 200)  # Расположение иконки Калькулятора
