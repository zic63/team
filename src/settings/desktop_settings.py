import json
import os

class DesktopSettings:
    SETTINGS_FILE = 'settings/desktop_settings.json'

    def __init__(self):
        # Проверяем наличие папки и создаем её, если она отсутствует
        settings_dir = os.path.dirname(self.SETTINGS_FILE)
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir)

        self.toggleFilesAction = None
        self.togglePlayerAction = None
        self.toggleTimelineAction = None
        self.filesPanel = None
        self.playerPanel = None
        self.timeline = None

    def save(self, settings):
        """Сохраняет настройки в файл."""
        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)

    def load(self):
        """Загружает настройки из файла."""
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {}

    def get_panel_visibility(self):
        """Возвращает видимость панелей и таймлайна."""
        settings = self.load()
        return {
            'filesPanel': settings.get('filesPanel', True),
            'playerPanel': settings.get('playerPanel', True),
            'timeline': settings.get('timeline', True),
        }

    def set_panel_visibility(self, filesPanel, playerPanel, timeline):
        """Сохраняет видимость панелей и таймлайна."""
        settings = {
            'filesPanel': filesPanel,
            'playerPanel': playerPanel,
            'timeline': timeline,
        }
        self.save(settings)

    def set_actions_and_panels(self, toggleFilesAction, togglePlayerAction, toggleTimelineAction, filesPanel, playerPanel, timeline):
        """Устанавливает действия и панели для управления видимостью."""
        self.toggleFilesAction = toggleFilesAction
        self.togglePlayerAction = togglePlayerAction
        self.toggleTimelineAction = toggleTimelineAction
        self.filesPanel = filesPanel
        self.playerPanel = playerPanel
        self.timeline = timeline

    def toggleFilesPanel(self):
        """Переключает видимость панели файлов."""
        if self.filesPanel and self.toggleFilesAction:
            self.filesPanel.setVisible(self.toggleFilesAction.isChecked())

    def togglePlayerPanel(self):
        """Переключает видимость панели медиаплеера."""
        if self.playerPanel and self.togglePlayerAction:
            self.playerPanel.setVisible(self.togglePlayerAction.isChecked())

    def toggleTimelinePanel(self):
        """Переключает видимость таймлайна."""
        if self.timeline and self.toggleTimelineAction:
            self.timeline.setVisible(self.toggleTimelineAction.isChecked())

    def close_event(self, event):
        """Сохраняет настройки при закрытии окна."""
        self.save_settings()
        event.accept()  # Принять событие закрытия

    def save_settings(self):
        """Сохраняет состояние видимости панелей и таймлайна."""
        self.set_panel_visibility(
            self.toggleFilesAction.isChecked(),
            self.togglePlayerAction.isChecked(),
            self.toggleTimelineAction.isChecked()
        )

    def load_settings(self):
        """Загружает настройки видимости панелей и таймлайна."""
        visibility = self.get_panel_visibility()
        if self.toggleFilesAction:
            self.toggleFilesAction.setChecked(visibility.get('filesPanel', True))
        if self.togglePlayerAction:
            self.togglePlayerAction.setChecked(visibility.get('playerPanel', True))
        if self.toggleTimelineAction:
            self.toggleTimelineAction.setChecked(visibility.get('timeline', True))

        # Устанавливаем видимость панелей и таймлайна в соответствии с сохраненными настройками
        self.toggleFilesPanel()
        self.togglePlayerPanel()
        self.toggleTimelinePanel()
