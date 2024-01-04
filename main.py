import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class BrowserTab(QWebEngineView):
    def __init__(self):
        super(BrowserTab, self).__init__()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.create_tab('http://armansite.neocities.org')

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.current_browser().back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.current_browser().forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.current_browser().reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.progress_bar = QProgressBar()
        self.statusBar().addWidget(self.progress_bar)

        # Hide the '+' icon on the first tab
        self.tabs.tabBar().tabButton(0, QTabBar.RightSide).hide()

    def create_tab(self, url):
        browser_tab = BrowserTab()
        browser_tab.setUrl(QUrl(url))
        browser_tab.urlChanged.connect(self.update_url)
        browser_tab.titleChanged.connect(self.update_title)
        browser_tab.iconChanged.connect(self.update_favicon)
        browser_tab.loadProgress.connect(self.update_progress)
        self.tabs.addTab(browser_tab, "New Tab")
        self.tabs.setCurrentWidget(browser_tab)

        # Hide the '+' icon on all tabs
        for i in range(self.tabs.count() - 1):
            button = self.tabs.tabBar().tabButton(i, QTabBar.RightSide)
            if button is not None:
                button.hide()

        # Show the '+' icon only on the last tab
        last_button = self.tabs.tabBar().tabButton(self.tabs.count() - 1, QTabBar.RightSide)
        if last_button is not None:
            last_button.show()

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        self.tabs.removeTab(index)

        # If the last tab is closed, close the entire browser
        if self.tabs.count() == 0:
            self.close()

    def navigate_home(self):
        self.current_browser().setUrl(QUrl('http://armansite.neocities.org'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_title(self, title):
        index = self.tabs.indexOf(self.sender())
        self.tabs.setTabText(index, title)

    def update_favicon(self, icon):
        index = self.tabs.indexOf(self.sender())
        self.tabs.setTabIcon(index, icon)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

app = QApplication(sys.argv)
QApplication.setApplicationName('StellarSurf')
window = MainWindow()
window.showMaximized()
app.exec_()
