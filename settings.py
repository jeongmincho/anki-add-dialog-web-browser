from aqt.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton
)
from . import config

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Dialog Web Browser")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.setMinimumWidth(400)
        
        url_layout = QHBoxLayout()
        url_label = QLabel("Start URL:")
        self.url_input = QLineEdit()
        self.url_input.setText(config.get_config()["start_url"])
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def save_settings(self):
        cfg = config.get_config()
        cfg["start_url"] = self.url_input.text()
        config.save_config(cfg)
        self.accept()
