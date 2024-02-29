import sys
import json
import requests
from bs4 import BeautifulSoup as bs
import mpv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import locale

class MainWindow(QMainWindow, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("InterVision")
        self.layout = QHBoxLayout()
        self.channels = {
            "BNT 1": "watch_bnt1",
            "BNT 2": "watch_bnt2",
            "BNT 3": "watch_bnt3",
            "BNT 4": "watch_bnt4",
            "bTV": "watch_btv",
            "Nova": "watch_nova",
            "Korea Central TV": "watch_nkctv",
            "WCBS": "watch_wcbs",
            "TRT 1": "watch_trt1"
        }
        # Create a widget for the channel selection elements
        channel_selection_widget = QWidget()
        channel_layout = QVBoxLayout()
        channel_selection_widget.setLayout(channel_layout)
        self.channel_dropdown = QComboBox(self)
        self.channel_dropdown.addItems(self.channels.keys())
        channel_layout.addWidget(self.channel_dropdown)
        self.play_btn = QPushButton("Play", self)
        self.play_btn.clicked.connect(self.play_selected_channel)
        channel_layout.addWidget(self.play_btn)
        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.clicked.connect(self.stop_playing)
        self.stop_btn.setEnabled(False)
        channel_layout.addWidget(self.stop_btn)
        self.layout.addWidget(channel_selection_widget)

        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)
        
#class MainWindow(QMainWindow, QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)
#        self.setWindowTitle("InterVision")
#        self.layout = QVBoxLayout()
#        self.channels = {
#            "BNT 1": "watch_bnt1",
#            "BNT 2": "watch_bnt2",
#            "BNT 3": "watch_bnt3",
#            "BNT 4": "watch_bnt4",
#            "bTV": "watch_btv",
#            "Nova": "watch_nova",
#            "Korea Central TV": "watch_nkctv",
#            "WCBS": "watch_wcbs",
#            "TRT 1": "watch_trt1"
#        }
#        self.current_channel = None
#        self.player = None
#        # Add channel dropdown
#        self.channel_dropdown = QComboBox(self)
#        self.channel_dropdown.addItems(self.channels.keys())
#        self.layout.addWidget(self.channel_dropdown)

        # Add play and stop buttons
#        self.play_btn = QPushButton("Play", self)
#        self.play_btn.clicked.connect(self.play_selected_channel)
#        self.layout.addWidget(self.play_btn)

#        self.stop_btn = QPushButton("Stop", self)
#        self.stop_btn.clicked.connect(self.stop_playing)
#        self.stop_btn.setEnabled(False)
#        self.layout.addWidget(self.stop_btn)

#        self.container = QWidget(self)
#        self.setCentralWidget(self.container)
#        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
#        self.container.setAttribute(Qt.WA_NativeWindow)

#        self.setLayout(self.layout)

    def play_selected_channel(self):
        if self.player != None:
            self.stop_playing()

        selected_channel = self.channel_dropdown.currentText()
        try:
            method_name = self.channels[selected_channel]
            getattr(self, method_name)()
            self.current_channel = selected_channel
            self.play_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        except Exception as e:
            self.show_error_message(str(e))

    def stop_playing(self):
        if self.player != None:
            self.player.terminate()
            self.player = None
            self.play_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.current_channel = None

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def watch_btv(self):
        url = "https://btvplus.bg/lbin/v3/btvplus/player_config.php?media_id=2110383625&_=1707071392775"
        response = requests.get(url, headers={"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br"})
        response_json = response.json()
        media_url = response_json['info']['file'].replace(".m3u8", "_low.m3u8")
        wheaders="Referer: http://btvplus.bg, Origin: http://btvplus.bg"
        print(media_url)
        self.play_with_mpv(media_url,wheaders)

    def watch_bnt1(self):
        url = "http://i.cdn.bg/live/4eViE8vGzI"
        response = requests.get(url, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Referer": "http://tv.bnt.bg/", "Upgrade-Insecure-Requests": "1"})
        parsed_html = bs(response.text, 'html.parser')
        source_tag = parsed_html.find('video', {'id': 'player_1'}).find('source')
        media_url = "http:" + source_tag['src']
        wheaders="Referer: http://i.cdn.bg, Origin: http://i.cdn.bg"
        self.play_with_mpv(media_url,wheaders)

    def watch_bnt2(self):
        url = "http://i.cdn.bg/live/ZBPbdxDHm7"
        response = requests.get(url, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Referer": "http://tv.bnt.bg/", "Upgrade-Insecure-Requests": "1"})
        parsed_html = bs(response.text, 'html.parser')
        source_tag = parsed_html.find('video', {'id': 'player_1'}).find('source')
        media_url = "http:" + source_tag['src']
        wheaders="Referer: http://i.cdn.bg, Origin: http://i.cdn.bg"
        self.play_with_mpv(media_url,wheaders)

    def watch_bnt3(self):
        url = "http://i.cdn.bg/live/OQ70Ds9Lcp"
        response = requests.get(url, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Referer": "http://tv.bnt.bg/", "Upgrade-Insecure-Requests": "1"})
        parsed_html = bs(response.text, 'html.parser')
        source_tag = parsed_html.find('video', {'id': 'player_1'}).find('source')
        media_url = "http:" + source_tag['src']
        wheaders="Referer: http://i.cdn.bg, Origin: http://i.cdn.bg"
        self.play_with_mpv(media_url,wheaders)

    def watch_bnt4(self):
        url = "http://i.cdn.bg/live/ls4wHAbTmY"
        response = requests.get(url, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Referer": "http://tv.bnt.bg/", "Upgrade-Insecure-Requests": "1"})
        parsed_html = bs(response.text, 'html.parser')
        source_tag = parsed_html.find('video', {'id': 'player_1'}).find('source')
        media_url = "http:" + source_tag['src']
        wheaders="Referer: http://i.cdn.bg, Origin: http://i.cdn.bg"
        self.play_with_mpv(media_url,wheaders)

    def watch_nova(self):
        url = "https://i.cdn.bg/live/0OmMKJ4SgY"
        response = requests.get(url, headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "keep-alive", "Referer": "https://nova.bg/", "Upgrade-Insecure-Requests": "1"})
        parsed_html = bs(response.text, 'html.parser')
        source_tag = parsed_html.find('video').find('source')
        media_url = source_tag['src']
        wheaders="Referer: http://i.cdn.bg, Origin: http://i.cdn.bg"
        self.play_with_mpv(media_url,wheaders)

    def watch_nkctv(self):
        wheaders="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        self.play_with_mpv("https://tv.nknews.org/tvdash/stream.mpd",wheaders)

    def watch_wcbs(self):
        url = "https://www.cbsnews.com/live/"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br"})
        parsed_html = bs(response.text, 'html.parser')
        script = str(parsed_html.find_all('script')[7].string)
        var_str = script.split('\n')[2][script.split('\n')[2].find('{'):]
        cbsnews_defaultpayload = json.loads(var_str)
        media_url=cbsnews_defaultpayload['items'][0]['video']
        wheaders="Referer: https://www.cbsnews.com/, Origin: https://www.cbsnews.com/, User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        self.play_with_mpv(media_url,wheaders)

    def watch_trt1(self):
        url="https://trt.daioncdn.net/trt-1/master.m3u8?app=clean"
        self.play_with_mpv(url,"")

    def play_with_mpv(self, media_url, wheaders):
        try:
            locale.setlocale(locale.LC_NUMERIC,"C")
            self.player = mpv.MPV(id=str(int(self.container.winId())),
                vo='x11',
                log_handler=print,
                loglevel='debug',
                http_header_fields=wheaders)
            self.player.play(media_url)
        except Exception as e:
            self.show_error_message(str(e))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

