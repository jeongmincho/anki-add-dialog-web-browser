from aqt import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineSettings, Qt, QUrl
from aqt.qt import QWidget, QVBoxLayout

class BrowserWidget(QWidget):
    def __init__(self, url="https://www.google.com", parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.profile = QWebEngineProfile("browser_profile")
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        
        self.webview = QWebEngineView(self)
        self.webpage = QWebEnginePage(self.profile, self.webview)
        self.webview.setPage(self.webpage)
        self.webview.load(QUrl(url))
        
        layout.addWidget(self.webview)
