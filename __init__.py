from aqt import QSplitter, Qt, gui_hooks, mw
from aqt.qt import QWidget, QVBoxLayout, QShortcut, QKeySequence, QAction
from aqt.utils import tooltip
from .browser import BrowserWidget
from . import config
from .settings import SettingsDialog

def show_settings():
    dialog = SettingsDialog(mw)
    dialog.exec()

def show_browser_sidebar(editor):
    parent = editor.parentWindow
    
    if hasattr(parent, '_browser_sidebar'):
        if parent._browser_sidebar.isVisible():
            parent._browser_sidebar.hide()
            return
        else:
            parent._browser_sidebar.show()
            return
    
    splitter = QSplitter(Qt.Orientation.Horizontal)
    parent._splitter = splitter
    
    main_widget = parent
    old_layout = main_widget.layout()
    
    container = QWidget()
    container.setLayout(old_layout)
    
    splitter.addWidget(container)
    browser = BrowserWidget(url=config.get_config()["start_url"], parent=parent)
    parent._browser_sidebar = browser
    splitter.addWidget(browser)
    
    new_layout = QVBoxLayout()
    new_layout.setContentsMargins(0, 0, 0, 0)
    new_layout.addWidget(splitter)
    main_widget.setLayout(new_layout)
    
    splitter.setSizes([500, 500])

def add_browser_button(buttons, editor):
    button = editor.addButton(
        icon=None,
        cmd="toggle_browser",
        func=lambda e: show_browser_sidebar(editor),
        tip="Toggle web browser (⌘⇧B)",  
        label="🌐"
    )

    shortcut = QShortcut(QKeySequence("Shift+Ctrl+B"), editor.widget)
    shortcut.activated.connect(lambda: show_browser_sidebar(editor))

    buttons.append(button)
    return buttons

settings_action = QAction("Add Dialog Web Browser", mw)
settings_action.triggered.connect(show_settings)
mw.form.menuTools.addAction(settings_action)

gui_hooks.editor_did_init_buttons.append(add_browser_button)
