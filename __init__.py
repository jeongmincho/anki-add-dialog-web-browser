from aqt import QSplitter, Qt, gui_hooks
from aqt.qt import QWidget, QVBoxLayout, QShortcut, QKeySequence
from aqt.utils import tooltip
from .browser import BrowserWidget

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
    
    editor_widget = editor.widget
    old_parent = editor_widget.parent()
    splitter.addWidget(editor_widget)
    
    browser = BrowserWidget(parent=parent)
    parent._browser_sidebar = browser
    splitter.addWidget(browser)
    
    editor_container = old_parent
    container_layout = editor_container.layout()
    if not container_layout:
        container_layout = QVBoxLayout(editor_container)
    container_layout.addWidget(splitter)
    
    splitter.setSizes([500, 500])

def add_browser_button(buttons, editor):
    button = editor.addButton(
        icon=None,
        cmd="toggle_browser",
        func=lambda e: show_browser_sidebar(editor),
        tip="Toggle browser sidebar (⌘⇧B)",  
        label="🌐"
    )

    shortcut = QShortcut(QKeySequence("Shift+Ctrl+B"), editor.widget)
    shortcut.activated.connect(lambda: show_browser_sidebar(editor))

    buttons.append(button)
    return buttons

gui_hooks.editor_did_init_buttons.append(add_browser_button)
