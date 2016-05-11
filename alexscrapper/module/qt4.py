import sys
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage 

from lxml import html

class Render(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()


class PYQTPageRenderor(object):
    def __init__(self, url):
        self.url = url

    # url = 'https://www.mileageplanshopping.com/b____.htm'
    # r       = Render(url)
    # result  = r.frame.toHtml()
    # body    = r.frame.toHtml()
    # formatted_body = str(result.toAscii())
    # print formatted_body
    # tree = html.fromstring(formatted_body)
    # print tree.body
    # div     = tree.xpath('//div[@class="mn_merchantGroup"]')
    # print len(div)
