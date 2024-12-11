from aqt import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings, Qt, QUrl
from aqt.qt import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QShortcut, QKeySequence

class BrowserWidget(QWidget):
    def __init__(self, url="https://www.google.com", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)
        
        self.back_button = QPushButton("←", self)
        self.back_button.clicked.connect(self._go_back)
        self.back_button.setMaximumWidth(30)
        nav_layout.addWidget(self.back_button)

        self.forward_button = QPushButton("→", self)
        self.forward_button.clicked.connect(self._go_forward)
        self.forward_button.setMaximumWidth(30)
        nav_layout.addWidget(self.forward_button)

        self.reload_button = QPushButton("↻", self)
        self.reload_button.clicked.connect(self._reload_page)
        self.reload_button.setMaximumWidth(30)
        nav_layout.addWidget(self.reload_button)
        
        self.url_edit = QLineEdit(self)
        self.url_edit.returnPressed.connect(self._navigate_to_url)
        self.url_edit.setCursorPosition(0) 
        self.url_edit.setAlignment(Qt.AlignmentFlag.AlignLeft) 
        nav_layout.addWidget(self.url_edit)
        
        QShortcut(QKeySequence("Ctrl+["), self).activated.connect(self._go_back)
        QShortcut(QKeySequence("Ctrl+]"), self).activated.connect(self._go_forward)
        QShortcut(QKeySequence("Ctrl+L"), self).activated.connect(self._focus_url)
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self._reload_page)
        
        layout.addLayout(nav_layout)
        
        self.profile = QWebEngineProfile("browser_profile")
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        
        self.webview = QWebEngineView(self)
        self.webpage = QWebEnginePage(self.profile, self.webview)
        self.webview.setPage(self.webpage)
        
        self.webview.urlChanged.connect(self._url_changed)
        self.webview.loadFinished.connect(self._on_load_finished)
        
        self.webview.load(QUrl(url))
        self.url_edit.setText(url)
        
        layout.addWidget(self.webview)
    
    def _go_back(self):
        self.webview.back()

    def _go_forward(self):
        self.webview.forward()
    
    def _navigate_to_url(self):
        url = self.url_edit.text().strip()
        
        if any([
            url.startswith(('http://', 'https://')),
            url.startswith('www.'),
            '.' in url and not ' ' in url
        ]):
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
        else:
            url = 'https://www.google.com/search?q=' + url.replace(' ', '+')
            
        self.webview.setUrl(QUrl(url))
    
    def _url_changed(self, url):
        self.url_edit.setText(url.toString())
        self.url_edit.setCursorPosition(0)

    def _focus_url(self):
        self.url_edit.setFocus()
        self.url_edit.selectAll()

    def _reload_page(self):
        self.webview.reload()

    def focus_web_content(self):
        self.webview.setFocus()

    def showEvent(self, event):
        super().showEvent(event)
        self.focus_web_content()

    def _on_load_finished(self, ok):
        if ok:
            self.focus_web_content()
