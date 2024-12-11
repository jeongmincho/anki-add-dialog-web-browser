from aqt.qt import QWidget, QVBoxLayout, QTextEdit, Qt, QPoint
from aqt import mw

class DebugWindow(QWidget):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DebugWindow()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Debug Window")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # Position window on the right side of the main window
        if mw:
            pos = mw.pos()
            self.move(pos.x() + mw.width(), pos.y())

    def log(self, message):
        self.text_edit.append(str(message))
        self.show()
        self.raise_()

debug_window = DebugWindow.get_instance()

def debug(message):
    debug_window.log(message)
