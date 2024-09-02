import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QAction, QMenuBar, QApplication, QFileDialog
from PyQt5.QtCore import Qt
from gui.desktop_files import Desktop as FilesDesktop
from gui.desktop_player import MediaPlayer
from gui.timeline import Timeline
from settings.desktop_settings import DesktopSettings
from project_file import ProjectFile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = DesktopSettings()  # Создаем объект для работы с настройками
        self.project_file = ProjectFile()  # Создаем объект для работы с файлами проекта
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
        fileMenu = menubar.addMenu('File')

        self.newProjectAction = QAction('New Project', self)
        self.newProjectAction.triggered.connect(self.createNewProject)
        fileMenu.addAction(self.newProjectAction)

        self.openProjectAction = QAction('Open Project', self)
        self.openProjectAction.triggered.connect(self.openProject)
        fileMenu.addAction(self.openProjectAction)

        viewMenu = menubar.addMenu('View')

        self.toggleFilesAction = QAction('Show Files Panel', self, checkable=True, checked=True)
        self.toggleFilesAction.triggered.connect(self.settings.toggleFilesPanel)
        viewMenu.addAction(self.toggleFilesAction)

        self.togglePlayerAction = QAction('Show Media Player', self, checkable=True, checked=True)
        self.togglePlayerAction.triggered.connect(self.settings.togglePlayerPanel)
        viewMenu.addAction(self.togglePlayerAction)

        self.toggleTimelineAction = QAction('Show Timeline', self, checkable=True, checked=True)
        self.toggleTimelineAction.triggered.connect(self.settings.toggleTimelinePanel)
        viewMenu.addAction(self.toggleTimelineAction)

        # Передаем действия и панели в DesktopSettings
        self.settings.set_actions_and_panels(
            self.toggleFilesAction,
            self.togglePlayerAction,
            self.toggleTimelineAction,
            self.filesPanel,
            self.playerPanel,
            self.timeline
        )

        self.settings.load_settings()  # Загружаем настройки при инициализации

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

    def createNewProject(self):
        """Создает новый проект."""
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Project File', '', 'Project Files (*.proj)')
        if file_name:
            self.project_file.create(file_name)
            # Можно добавить логику для очистки текущего проекта или начальной настройки нового проекта

    def openProject(self):
        """Открывает существующий проект."""
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Project File', '', 'Project Files (*.proj)')
        if file_name:
            project_data = self.project_file.load(file_name)
            # Логика для загрузки данных проекта в интерфейс

    def closeEvent(self, event):
        """Передает событие закрытия в DesktopSettings."""
        self.settings.save_settings()  # Сохраняем настройки при закрытии
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
