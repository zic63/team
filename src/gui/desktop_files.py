import json
import os
import sip  # Импортируем библиотеку sip для управления объектами Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QMenu, QMessageBox, QInputDialog, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout
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
        menu = QMenu()
        menu.addAction('Открыть', self.open)
        menu.addAction('Переименовать', self.rename)
        menu.addAction('Удалить', self.delete)
        menu.exec_(self.mapToGlobal(position))

    def open(self):
        if os.path.exists(self.filePath):
            print(f"Открытие файла {self.text()}...")
        else:
            QMessageBox.warning(self, "Ошибка", f"Файл {self.text()} не найден!")

    def rename(self):
        newName, ok = QInputDialog.getText(self, 'Переименовать иконку', 'Введите новое имя:')
        if ok and newName:
            self.setText(newName)

    def delete(self):
        if os.path.exists(self.filePath):
            reply = QMessageBox.question(self, 'Удалить файл',
                                         f"Вы уверены, что хотите удалить файл {self.text()}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    os.remove(self.filePath)
                    self.deleteLater()
                    QMessageBox.information(self, "Успех", f"Файл {self.text()} успешно удален!")
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось удалить файл: {e}")
        else:
            reply = QMessageBox.question(self, 'Удалить иконку',
                                         f"Файл {self.text()} не найден. Удалить иконку?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.deleteLater()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        parent = self.parent()
        while parent and not isinstance(parent, Desktop):
            parent = parent.parent()
        if parent:
            for folder in parent.folders:
                if folder and not sip.isdeleted(folder):
                    if folder.geometry().adjusted(-20, -20, 20, 20).contains(self.geometry().center()):
                        folder.addIcon(self)
                        return

    def getIconState(self):
        return {
            'name': self.text(),
            'filePath': self.filePath,
            'position': (self.x(), self.y())
        }

class FolderWindow(QWidget):
    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'Папка: {folder.text()}')
        self.setGeometry(300, 300, 600, 400)
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
            item.setParent(self.folder)
            item.hide()

class DesktopFolder(QPushButton):
    def __init__(self, name, position, parent=None):
        super().__init__(name, parent)
        self.setFixedSize(100, 50)
        self.move(position)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
        self.icons = []
        self.oldPos = self.pos()

    def openMenu(self, position):
        menu = QMenu()
        menu.addAction('Открыть', self.openFolder)
        menu.addAction('Переименовать', self.rename)
        menu.addAction('Удалить', self.delete)
        menu.exec_(self.mapToGlobal(position))

    def openFolder(self):
        self.folderWindow = FolderWindow(self, self.parent())
        self.folderWindow.show()

    def rename(self):
        newName, ok = QInputDialog.getText(self, 'Переименовать папку', 'Введите новое имя:')
        if ok and newName:
            self.setText(newName)

    def delete(self):
        reply = QMessageBox.question(self, 'Удалить папку',
                                     f"Вы уверены, что хотите удалить папку {self.text()}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for icon in self.icons:
                icon.deleteLater()
            self.deleteLater()
            QMessageBox.information(self, "Успех", f"Папка {self.text()} успешно удалена!")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def addIcon(self, icon):
        self.icons.append(icon)
        icon.hide()

    def getFolderState(self):
        return {
            'name': self.text(),
            'position': (self.x(), self.y()),
            'icons': [icon.getIconState() for icon in self.icons if icon and not sip.isdeleted(icon)]
        }

class Desktop(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icons = []
        self.folders = []
        self.setupIcons()

        self.taskbar = QWidget(self)
        self.taskbar.setFixedHeight(40)
        self.taskbar.setStyleSheet("background-color: darkblue; border-top: 2px solid black;")

        startBtn = QPushButton('Пуск', self.taskbar)
        startBtn.setFixedSize(100, 30)

        startMenu = QMenu(self)
        startMenu.addAction('Создать иконку', self.createIcon)
        startMenu.addAction('Создать папку', self.createFolder)

        startBtn.clicked.connect(lambda: self.showStartMenu(startMenu, startBtn))

        hbox = QHBoxLayout(self.taskbar)
        hbox.addWidget(startBtn)
        hbox.addStretch(1)
        hbox.setContentsMargins(5, 5, 5, 5)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.taskbar)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def showStartMenu(self, menu, button):
        menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))

    def setupIcons(self):
        if os.path.exists('desktop_state.json'):
            with open('desktop_state.json', 'r') as f:
                data = json.load(f)

                for folderData in data.get('folders', []):
                    folder = self.createDesktopFolder(folderData['name'], QPoint(*folderData['position']))
                    for iconData in folderData.get('icons', []):
                        existing_icon = next((icon for icon in self.icons if icon.filePath == iconData['filePath']), None)
                        if existing_icon:
                            folder.addIcon(existing_icon)
                        else:
                            icon = self.createDesktopIcon(iconData['name'], iconData['filePath'], QPoint(*iconData['position']))
                            folder.addIcon(icon)

                for iconData in data.get('icons', []):
                    existing_icon = next((icon for icon in self.icons if icon.filePath == iconData['filePath']), None)
                    if not existing_icon:
                        self.createDesktopIcon(iconData['name'], iconData['filePath'], QPoint(*iconData['position']))

    def createDesktopIcon(self, name, filePath, position=QPoint(50, 50)):
        icon = DesktopIcon(name, filePath, position, self)
        icon.show()
        self.icons.append(icon)
        return icon

    def createDesktopFolder(self, name, position=QPoint(50, 50)):
        folder = DesktopFolder(name, position, self)
        folder.show()
        self.folders.append(folder)
        return folder

    def createIcon(self):
        name, ok = QInputDialog.getText(self, 'Создать иконку', 'Введите имя иконки:')
        if ok and name:
            self.createDesktopIcon(name, '', QPoint(50, 50))

    def createFolder(self):
        name, ok = QInputDialog.getText(self, 'Создать папку', 'Введите имя папки:')
        if ok and name:
            self.createDesktopFolder(name, QPoint(50, 50))

    def closeEvent(self, event):
        data = {
            'icons': [icon.getIconState() for icon in self.icons if icon and not sip.isdeleted(icon)],
            'folders': [folder.getFolderState() for folder in self.folders if folder and not sip.isdeleted(folder)]
        }
        with open('desktop_state.json', 'w') as f:
            json.dump(data, f, indent=4)
        super().closeEvent(event)
