import json
import os

class ProjectFile:
    def __init__(self):
        self.file_path = None

    def create(self, file_path):
        self.file_path = file_path
        self.save({})

    def save(self, data):
        if self.file_path:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)

    def load(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
