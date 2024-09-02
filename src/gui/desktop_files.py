import json
import os
import sip  # Импортируем библиотеку sip для управления объектами Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QMenu, QMessageBox, 
                             QInputDialog, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout)
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
        menu = QMenu()  # Создаем контекстное меню
        menu.addAction('Открыть', self.open)  # Добавляем действие "Открыть"
        menu.addAction('Переименовать', self.rename)  # Добавляем действие "Переименовать"
        menu.addAction('Удалить', self.delete)  # Добавляем действие "Удалить"
        menu.exec_(self.mapToGlobal(position))  # Показываем меню в глобальных координатах

    def open(self):
        if os.path.exists(self.filePath):  # Проверяем существование файла
            print(f"Открытие файла {self.text()}...")
        else:
            QMessageBox.warning(self, "Ошибка", f"Файл {self.text()} не найден!")  # Показываем предупреждение, если файл не найден

    def rename(self):
        newName, ok = QInputDialog.getText(self, 'Переименовать иконку', 'Введите новое имя:')  # Запрашиваем новое имя
        if ok and newName:
            self.setText(newName)  # Устанавливаем новое имя иконки

    def delete(self):
        if os.path.exists(self.filePath):  # Проверяем существование файла
            reply = QMessageBox.question(self, 'Удалить файл',
                                         f"Вы уверены, что хотите удалить файл {self.text()}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # Запрашиваем подтверждение на удаление
            if reply == QMessageBox.Yes:
                try:
                    os.remove(self.filePath)  # Пытаемся удалить файл
                    self.deleteLater()  # Удаляем иконку
                    QMessageBox.information(self, "Успех", f"Файл {self.text()} успешно удален!")  # Показываем сообщение об успешном удалении
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось удалить файл: {e}")  # Показываем сообщение об ошибке, если не удалось удалить файл
        else:
            reply = QMessageBox.question(self, 'Удалить иконку',
                                         f"Файл {self.text()} не найден. Удалить иконку?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # Запрашиваем подтверждение на удаление иконки
            if reply == QMessageBox.Yes:
                self.deleteLater()  # Удаляем иконку

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()  # Сохраняем позицию мыши при нажатии

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)  # Вычисляем изменение позиции
            self.move(self.x() + delta.x(), self.y() + delta.y())  # Перемещаем иконку
            self.oldPos = event.globalPos()  # Обновляем позицию мыши

    def mouseReleaseEvent(self, event):
        parent = self.parent()
        while parent and not isinstance(parent, Desktop):
            parent = parent.parent()  # Находим рабочий стол в иерархии родительских виджетов
        if parent:
            for folder in parent.folders:
                if folder and not sip.isdeleted(folder):
                    if folder.geometry().adjusted(-20, -20, 20, 20).contains(self.geometry().center()):
                        folder.addIcon(self)  # Добавляем иконку в папку, если она находится в пределах ее области
                        return

    def getIconState(self):
        return {
            'name': self.text(),
            'filePath': self.filePath,
            'position': (self.x(), self.y())
        }  # Возвращаем состояние иконки для сохранения

class FolderWindow(QWidget):
    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Папка: {folder.text()}')  # Устанавливаем заголовок окна папки
        self.setGeometry(300, 300, 600, 400)  # Устанавливаем размеры и положение окна
        layout = QVBoxLayout(self)
        self.folder = folder

        folderNameLabel = QLabel(f'Содержимое папки "{folder.text()}":', self)
        layout.addWidget(folderNameLabel)

        self.iconLayout = QVBoxLayout()

        for item in folder.icons:
            item.setParent(self)
            item.show()
            self.iconLayout.addWidget(item)

        layout.addLayout(self.iconLayout)
        self.setLayout(layout)

    def closeEvent(self, event):
        for item in self.iconLayout.children():
            item.setParent(self.folder)  # Возвращаем иконки в родительскую папку
            item.hide()
        super().closeEvent(event)  # Вызываем базовый метод

class DesktopFolder(QPushButton):
    def __init__(self, name, position, parent=None):
        super().__init__(name, parent)
        self.setFixedSize(100, 50)
        self.move(position)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
        self.icons = []  # Список иконок в папке
        self.oldPos = self.pos()

    def openMenu(self, position):
        menu = QMenu()  # Создаем контекстное меню
        menu.addAction('Открыть', self.openFolder)  # Добавляем действие "Открыть"
        menu.addAction('Переименовать', self.rename)  # Добавляем действие "Переименовать"
        menu.addAction('Удалить', self.delete)  # Добавляем действие "Удалить"
        menu.exec_(self.mapToGlobal(position))  # Показываем меню в глобальных координатах

    def openFolder(self):
        self.folderWindow = FolderWindow(self, self.parent())  # Создаем и показываем окно папки
        self.folderWindow.show()

    def rename(self):
        newName, ok = QInputDialog.getText(self, 'Переименовать папку', 'Введите новое имя:')  # Запрашиваем новое имя папки
        if ok and newName:
            self.setText(newName)  # Устанавливаем новое имя папки

    def delete(self):
        reply = QMessageBox.question(self, 'Удалить папку',
                                     f"Вы уверены, что хотите удалить папку {self.text()}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)  # Запрашиваем подтверждение на удаление папки
        if reply == QMessageBox.Yes:
            for icon in self.icons:
                icon.deleteLater()  # Удаляем все иконки в папке
            self.deleteLater()  # Удаляем папку
            QMessageBox.information(self, "Успех", f"Папка {self.text()} успешно удалена!")  # Показываем сообщение об успешном удалении

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()  # Сохраняем позицию мыши при нажатии

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)  # Вычисляем изменение позиции
            self.move(self.x() + delta.x(), self.y() + delta.y())  # Перемещаем папку
            self.oldPos = event.globalPos()  # Обновляем позицию мыши

    def addIcon(self, icon):
        self.icons.append(icon)  # Добавляем иконку в папку
        icon.hide()

    def getFolderState(self):
        return {
            'name': self.text(),
            'position': (self.x(), self.y()),
            'icons': [icon.getIconState() for icon in self.icons if icon and not sip.isdeleted(icon)]
        }  # Возвращаем состояние папки для сохранения

class Desktop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icons = []
        self.folders = []
        self.setupIcons()  # Настраиваем иконки

        self.taskbar = QWidget(self)
        self.taskbar.setFixedHeight(40)
        
        # Устанавливаем стиль панели задач

        startBtn = QPushButton('Пуск', self.taskbar)
        startBtn.setFixedSize(100, 30)

        startMenu = QMenu(self)
        startMenu.addAction('Создать иконку', self.createIcon)  # Добавляем действие "Создать иконку"
        startMenu.addAction('Создать папку', self.createFolder)  # Добавляем действие "Создать папку"

        startBtn.clicked.connect(lambda: self.showStartMenu(startMenu, startBtn))  # Подключаем кнопку "Пуск" к меню

        hbox = QHBoxLayout(self.taskbar)
        hbox.addWidget(startBtn)
        hbox.addStretch(1)
        hbox.setContentsMargins(5, 5, 5, 5)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.taskbar)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def showStartMenu(self, menu, button):
        menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))  # Показываем меню "Пуск" в глобальных координатах

    def setupIcons(self):
        if os.path.exists('desktop_state.json'):
            with open('desktop_state.json', 'r') as f:
                data = json.load(f)

                for folderData in data.get('folders', []):
                    folder = self.createDesktopFolder(folderData['name'], QPoint(*folderData['position']))
                    for iconData in folderData.get('icons', []):
                        existing_icon = next((icon for icon in self.icons if icon.filePath == iconData['filePath']), None)
                        if existing_icon:
                            folder.addIcon(existing_icon)  # Добавляем существующую иконку в папку
                        else:
                            icon = self.createDesktopIcon(iconData['name'], iconData['filePath'], QPoint(*iconData['position']))
                            folder.addIcon(icon)  # Создаем новую иконку и добавляем ее в папку

                for iconData in data.get('icons', []):
                    existing_icon = next((icon for icon in self.icons if icon.filePath == iconData['filePath']), None)
                    if not existing_icon:
                        self.createDesktopIcon(iconData['name'], iconData['filePath'], QPoint(*iconData['position']))  # Создаем иконку, если ее еще нет

    def createDesktopIcon(self, name, filePath, position=QPoint(50, 50)):
        icon = DesktopIcon(name, filePath, position, self)
        icon.show()
        self.icons.append(icon)  # Добавляем иконку на рабочий стол
        return icon

    def createDesktopFolder(self, name, position=QPoint(50, 50)):
        folder = DesktopFolder(name, position, self)
        folder.show()
        self.folders.append(folder)  # Добавляем папку на рабочий стол
        return folder

    def createIcon(self):
        name, ok = QInputDialog.getText(self, 'Создать иконку', 'Введите имя иконки:')  # Запрашиваем имя новой иконки
        if ok and name:
            self.createDesktopIcon(name, '', QPoint(50, 50))  # Создаем новую иконку

    def createFolder(self):
        name, ok = QInputDialog.getText(self, 'Создать папку', 'Введите имя папки:')  # Запрашиваем имя новой папки
        if ok and name:
            self.createDesktopFolder(name, QPoint(50, 50))  # Создаем новую папку

    def closeEvent(self, event):
        data = {
            'icons': [icon.getIconState() for icon in self.icons if icon and not sip.isdeleted(icon)],
            'folders': [folder.getFolderState() for folder in self.folders if folder and not sip.isdeleted(folder)]
        }
        with open('desktop_state.json', 'w') as f:
            json.dump(data, f, indent=4)  # Сохраняем состояние рабочего стола в файл
        super().closeEvent(event)  # Вызываем базовый метод
