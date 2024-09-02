import os
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget

class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем объект медиаплеера и настраиваем его
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # Создаем виджет для отображения видео
        self.videoWidget = QVideoWidget()
        self.player.setVideoOutput(self.videoWidget)

        # Создаем кнопки управления
        self.playButton = QPushButton("Play")
        self.pauseButton = QPushButton("Pause")
        self.stopButton = QPushButton("Stop")
        self.openButton = QPushButton("Open File")

        # Подключаем сигналы кнопок к методам управления
        self.playButton.clicked.connect(self.play)
        self.pauseButton.clicked.connect(self.pause)
        self.stopButton.clicked.connect(self.stop)
        self.openButton.clicked.connect(self.openFile)

        # Создаем макет для размещения виджета видео и кнопок
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(self.stopButton)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        # Подключаем обработчик ошибок медиаплеера
        self.player.error.connect(self.handleError)

    def play(self):
        # Метод воспроизведения медиаплеера
        if self.player.state() == QMediaPlayer.PlayingState:
            print("Media is already playing.")
            return
        
        if self.playlist.mediaCount() > 0:
            self.player.play()
        else:
            print("No media loaded in playlist.")

    def pause(self):
        # Метод для приостановки воспроизведения
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            print("Media is not playing.")

    def stop(self):
        # Метод для остановки воспроизведения
        if self.player.state() in (QMediaPlayer.PlayingState, QMediaPlayer.PausedState):
            self.player.stop()
        else:
            print("Media is not playing or paused.")

    def openFile(self):
        # Метод для открытия файла и добавления его в плейлист
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if fileName:
            self.playlist.clear()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            # Включаем медиа плеер на воспроизведение
            self.player.play()
            
    def handleError(self):
        # Обработчик ошибок медиаплеера
        print(f"Error: {self.player.errorString()}")
