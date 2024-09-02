import sys
import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QAction, QMenuBar, QApplication
from PyQt5.QtCore import Qt
from gui.desktop_files import Desktop as FilesDesktop
from gui.desktop_player import MediaPlayer
from gui.timeline import Timeline  # Импортируем Timeline из timeline.py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()  # Инициализация пользовательского интерфейса

    def initUI(self):
        self.setWindowTitle('Симулятор Windows 98')  # Установка заголовка окна
        self.setGeometry(300, 300, 1600, 800)  # Установка размеров и положения окна

        # Основной виджет и компоновка
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)

        # Создаем разделитель, который будет содержать панели
        self.splitter = QSplitter(Qt.Horizontal)
        mainLayout.addWidget(self.splitter)

        # Создаем и добавляем панели файлов и медиаплеера
        self.filesPanel = self.createFilesPanel()
        self.playerPanel = self.createPlayerPanel()

        self.splitter.addWidget(self.filesPanel)
        self.splitter.addWidget(self.playerPanel)

        # Устанавливаем начальные размеры панелей
        self.splitter.setSizes([800, 800])

        # Создаем и добавляем таймлайн
        self.timeline = Timeline()
        mainLayout.addWidget(self.timeline)

        # Создаем меню и действия для управления видимостью панелей
        menubar = self.menuBar()
        viewMenu = menubar.addMenu('View')

        self.toggleFilesAction = QAction('Show Files Panel', self, checkable=True, checked=True)
        self.toggleFilesAction.triggered.connect(self.toggleFilesPanel)
        viewMenu.addAction(self.toggleFilesAction)

        self.togglePlayerAction = QAction('Show Media Player', self, checkable=True, checked=True)
        self.togglePlayerAction.triggered.connect(self.togglePlayerPanel)
        viewMenu.addAction(self.togglePlayerAction)

        self.toggleTimelineAction = QAction('Show Timeline', self, checkable=True, checked=True)
        self.toggleTimelineAction.triggered.connect(self.toggleTimelinePanel)
        viewMenu.addAction(self.toggleTimelineAction)

        self.loadSettings()  # Загружаем настройки при инициализации

    def createFilesPanel(self):
        panel = QWidget()
        panelLayout = QVBoxLayout(panel)
        panel.setStyleSheet("border: 1px solid darkgrey;")  # Стиль границы панели

        desktop = FilesDesktop(panel)
        desktop.setStyleSheet("background-color: lightblue;")  # Стиль фона панели
        panelLayout.addWidget(desktop)
        panelLayout.setContentsMargins(20, 20, 20, 20)  # Отступы внутри панели

        return panel

    def createPlayerPanel(self):
        panel = QWidget()
        panelLayout = QVBoxLayout(panel)
        panel.setStyleSheet("border: 1px solid darkgrey;")  # Стиль границы панели

        player = MediaPlayer()
        player.setStyleSheet("background-color: lightblue;")  # Стиль фона медиаплеера
        panelLayout.addWidget(player)
        panelLayout.setContentsMargins(20, 20, 20, 20)  # Отступы внутри панели

        return panel

    def toggleFilesPanel(self):
        """Переключает видимость панели файлов."""
        self.filesPanel.setVisible(self.toggleFilesAction.isChecked())

    def togglePlayerPanel(self):
        """Переключает видимость панели медиаплеера."""
        self.playerPanel.setVisible(self.togglePlayerAction.isChecked())

    def toggleTimelinePanel(self):
        """Переключает видимость таймлайна."""
        self.timeline.setVisible(self.toggleTimelineAction.isChecked())

    def closeEvent(self, event):
        """Сохраняет настройки при закрытии окна."""
        self.saveSettings()
        super().closeEvent(event)

    def saveSettings(self):
        """Сохраняет состояние видимости панелей и таймлайна в файл settings.json."""
        settings = {
            'filesPanel': self.toggleFilesAction.isChecked(),
            'playerPanel': self.togglePlayerAction.isChecked(),
            'timeline': self.toggleTimelineAction.isChecked(),
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def loadSettings(self):
        """Загружает настройки видимости панелей и таймлайна из файла settings.json."""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.toggleFilesAction.setChecked(settings.get('filesPanel', True))
                self.togglePlayerAction.setChecked(settings.get('playerPanel', True))
                self.toggleTimelineAction.setChecked(settings.get('timeline', True))

                # Устанавливаем видимость панелей и таймлайна в соответствии с сохраненными настройками
                self.toggleFilesPanel()
                self.togglePlayerPanel()
                self.toggleTimelinePanel()
        except FileNotFoundError:
            # Если файл настроек не найден, используем значения по умолчанию
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
