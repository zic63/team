# timeline.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize

class Timeline(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Создаем основной макет для таймлайна
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # Создаем область для прокрутки
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Создаем виджет содержимого для прокрутки
        self.contentWidget = QWidget()
        self.scrollArea.setWidget(self.contentWidget)

        # Создаем макет для виджета содержимого
        self.contentLayout = QHBoxLayout(self.contentWidget)
        self.contentLayout.setContentsMargins(5, 5, 5, 5)
        self.contentLayout.setSpacing(5)

        # Добавляем виджеты-клипы (пример)
        for i in range(10):
            clip = QPushButton(f'Clip {i + 1}', self.contentWidget)
            clip.setFixedSize(100, 40)
            self.contentLayout.addWidget(clip)

        # Добавляем область прокрутки в основной макет
        self.layout.addWidget(self.scrollArea)
        self.setFixedHeight(100)  # Устанавливаем фиксированную высоту для таймлайна

    def addClip(self, clip_name):
        # Метод для добавления нового клипа на таймлайн
        clip = QPushButton(clip_name, self.contentWidget)
        clip.setFixedSize(100, 40)
        self.contentLayout.addWidget(clip)
        self.contentWidget.adjustSize()  # Обновляем размер содержимого для корректной прокрутки
