import json
import os
import sip  # Импортируем библиотеку sip
from PyQt5.QtWidgets import QWidget, QPushButton, QMenu, QMessageBox, QInputDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint

class DesktopIcon(QPushButton):
    def __init__(self, name, filePath, position, parent=None):
        super().__init__(name, parent)
        self.filePath = filePath
        self.setFixedSize(100, 50)  # Устанавливаем фиксированный размер иконки
        self.move(position)  # Устанавливаем позицию иконки на рабочем столе
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Включаем контекстное меню
        self.customContextMenuRequested.connect(self.openMenu)  # Подключаем обработчик для открытия контекстного меню

        self.oldPos = self.pos()  # Сохраняем начальную позицию для перетаскивания

    def openMenu(self, position):
        # Открываем контекстное меню для иконки
        menu = QMenu()
        menu.addAction('Открыть', self.open)  # Добавляем опцию "Открыть"
        menu.addAction('Переименовать', self.rename)  # Добавляем опцию "Переименовать"
        menu.addAction('Удалить', self.delete)  # Добавляем опцию "Удалить"
        menu.exec_(self.mapToGlobal(position))  # Отображаем меню в глобальной позиции

    def open(self):
        # Обработчик для открытия файла
        if os.path.exists(self.filePath):
            print(f"Открытие файла {self.text()}...")
        else:
            QMessageBox.warning(self, "Ошибка", f"Файл {self.text()} не найден!")

    def rename(self):
        # Обработчик для переименования иконки
        newName, ok = QInputDialog.getText(self, 'Переименовать иконку', 'Введите новое имя:')
        if ok and newName:
            self.setText(newName)  # Устанавливаем новое имя иконки

    def delete(self):
        # Обработчик для удаления иконки и файла
        if os.path.exists(self.filePath):
            reply = QMessageBox.question(self, 'Удалить файл',
                                         f"Вы уверены, что хотите удалить файл {self.text()}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(self.filePath)  # Удаляем файл
                    self.deleteLater()  # Удаляем иконку с рабочего стола
                    QMessageBox.information(self, "Успех", f"Файл {self.text()} успешно удален!")
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось удалить файл: {e}")
        else:
            reply = QMessageBox.question(self, 'Удалить иконку',
                                         f"Файл {self.text()} не найден. Удалить иконку?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.deleteLater()  # Удаляем иконку с рабочего стола

    def mousePressEvent(self, event):
        # Обработчик нажатия мыши
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()  # Сохраняем глобальную позицию нажатия

    def mouseMoveEvent(self, event):
        # Обработчик перемещения мыши
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)  # Вычисляем разницу в позиции мыши
            self.move(self.x() + delta.x(), self.y() + delta.y())  # Перемещаем иконку
            self.oldPos = event.globalPos()  # Обновляем позицию

    def mouseReleaseEvent(self, event):
        # Проверяем, если иконка была отпущена над папкой, перемещаем её в папку
        parent = self.parent()
        while parent and not isinstance(parent, Desktop):
            parent = parent.parent()
        if parent:
            for folder in parent.folders:
                if folder and not sip.isdeleted(folder):  # Проверяем, что объект не был удален
                    if folder.geometry().adjusted(-20, -20, 20, 20).contains(self.geometry().center()):
                        folder.addIcon(self)
                        return

    def getIconState(self):
        # Метод для получения текущего состояния иконки (для сохранения)
        return {
            'name': self.text(),  # Имя иконки
            'filePath': self.filePath,  # Путь к файлу
            'position': (self.x(), self.y())  # Позиция иконки на рабочем столе
        }

class FolderWindow(QWidget):
    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Папка: {folder.text()}')
        self.setGeometry(300, 300, 600, 400)  # Устанавливаем размеры окна
        layout = QVBoxLayout(self)
        self.folder = folder

        # Добавляем метку с названием папки
        folderNameLabel = QLabel(f'Содержимое папки "{folder.text()}":', self)
        layout.addWidget(folderNameLabel)

        # Отображаем иконки и папки внутри папки
        self.iconLayout = QVBoxLayout()  # Макет для иконок и папок внутри окна

        for item in folder.icons:
            item.setParent(self)  # Меняем родителя, чтобы иконка или папка отображалась в новом окне
            item.show()
            self.iconLayout.addWidget(item)

        layout.addLayout(self.iconLayout)
        self.setLayout(layout)

    def closeEvent(self, event):
        # Возвращаем иконки и папки обратно в папку при закрытии окна
        for item in self.iconLayout.children():
            item.setParent(self.folder)
            item.hide()  # Скрываем элементы обратно в папке

class DesktopFolder(QPushButton):
    def __init__(self, name, position, parent=None):
        super().__init__(name, parent)
        self.setFixedSize(100, 50)  # Устанавливаем фиксированный размер папки
        self.move(position)  # Устанавливаем позицию папки на рабочем столе
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Включаем контекстное меню
        self.customContextMenuRequested.connect(self.openMenu)  # Подключаем обработчик для открытия контекстного меню
        self.icons = []  # Список для хранения иконок и папок внутри папки

        self.oldPos = self.pos()  # Сохраняем начальную позицию для перетаскивания

    def openMenu(self, position):
        # Открываем контекстное меню для папки
        menu = QMenu()
        menu.addAction('Открыть', self.openFolder)  # Добавляем опцию "Открыть"
        menu.addAction('Переименовать', self.rename)  # Добавляем опцию "Переименовать"
        menu.addAction('Удалить', self.delete)  # Добавляем опцию "Удалить"
        menu.exec_(self.mapToGlobal(position))  # Отображаем меню в глобальной позиции

    def openFolder(self):
        # Открытие папки в новом окне
        self.folderWindow = FolderWindow(self, self.parent())
        self.folderWindow.show()

    def rename(self):
        # Обработчик для переименования папки
        newName, ok = QInputDialog.getText(self, 'Переименовать папку', 'Введите новое имя:')
        if ok and newName:
            self.setText(newName)  # Устанавливаем новое имя папки

    def delete(self):
        # Обработчик для удаления папки
        reply = QMessageBox.question(self, 'Удалить папку',
                                     f"Вы уверены, что хотите удалить папку {self.text()}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for icon in self.icons:
                icon.deleteLater()  # Удаляем все иконки внутри папки
            self.deleteLater()  # Удаляем папку с рабочего стола
            QMessageBox.information(self, "Успех", f"Папка {self.text()} успешно удалена!")

    def mousePressEvent(self, event):
        # Обработчик нажатия мыши для папки
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()  # Сохраняем глобальную позицию нажатия

    def mouseMoveEvent(self, event):
        # Обработчик перемещения мыши для папки
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)  # Вычисляем разницу в позиции мыши
            self.move(self.x() + delta.x(), self.y() + delta.y())  # Перемещаем папку
            self.oldPos = event.globalPos()  # Обновляем позицию

    def addIcon(self, icon):
        # Добавляем иконку или папку в папку
        self.icons.append(icon)
        icon.hide()  # Скрываем иконку на рабочем столе, так как она теперь внутри папки

    def getFolderState(self):
        # Метод для получения текущего состояния папки (для сохранения)
        return {
            'name': self.text(),  # Имя папки
            'position': (self.x(), self.y()),  # Позиция папки на рабочем столе
            'icons': [icon.getIconState() for icon in self.icons if icon and not sip.isdeleted(icon)]  # Состояние иконок внутри папки
        }

class Desktop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icons = []  # Список для хранения всех иконок на рабочем столе
        self.folders = []  # Список для хранения всех папок на рабочем столе
        self.setupIcons()  # Инициализация иконок

    def setupIcons(self):
        # Загружаем иконки и папки из сохраненного состояния, если файл существует
        if os.path.exists('desktop_state.json'):
            if os.path.getsize('desktop_state.json') > 0:  # Проверка на пустоту файла
                with open('desktop_state.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):  # Проверяем, что data — это словарь
                        for folderData in data.get('folders', []):
                            folder = self.createDesktopFolder(folderData['name'], QPoint(*folderData['position']))
                            for iconData in folderData.get('icons', []):
                                icon = self.createDesktopIcon(iconData['name'], iconData['filePath'], QPoint(*iconData['position']))
                                folder.addIcon(icon)
                        for iconData in data.get('icons', []):
                            self.createDesktopIcon(iconData['name'], iconData['filePath'], QPoint(*iconData['position']))

    def createDesktopIcon(self, name, filePath, position=QPoint(50, 50)):
        # Метод для создания новой иконки на рабочем столе
        icon = DesktopIcon(name, filePath, position, self)
        icon.show()
        self.icons.append(icon)  # Добавляем иконку в список
        return icon

    def createDesktopFolder(self, name, position=QPoint(50, 50)):
        # Метод для создания новой папки на рабочем столе
        folder = DesktopFolder(name, position, self)
        folder.show()
        self.folders.append(folder)  # Добавляем папку в список
        return folder

    def saveDesktopState(self):
        # Метод для сохранения состояния всех иконок и папок на рабочем столе
        data = {
            'icons': [icon.getIconState() for icon in self.icons if icon and not sip.isdeleted(icon)],  # Проверяем, что иконка существует и не удалена
            'folders': [folder.getFolderState() for folder in self.folders if folder and not sip.isdeleted(folder)]  # Проверяем, что папка существует и не удалена
        }
        with open('desktop_state.json', 'w') as f:
            json.dump(data, f, indent=4)  # Сохраняем данные в файл в формате JSON
