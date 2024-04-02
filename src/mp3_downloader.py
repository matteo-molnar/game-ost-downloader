import os
import urllib.request as urllib2
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


class Mp3Downloader:
    BASE_URL = "https://downloads.khinsider.com"

    def __init__(self, ui_instance):
        self.ui = ui_instance

    def validate_url(self, url):
        if "//downloads.khinsider.com/game-soundtracks/album/" not in url:
            return False
        return True

    def create_directories(self, url, download_dir):
        url_parts = url.split("/")
        dir_name = download_dir + "/" + url_parts[len(url_parts) - 1]

        if not os.path.exists(download_dir):
            self.ui.update_log("INFO: creating directory: " + download_dir)
            os.makedirs(download_dir)
        if not os.path.exists(dir_name):
            self.ui.update_log("INFO: creating directory: " + dir_name)
            os.makedirs(dir_name)

        return dir_name

    def extract_song_links(self, url):
        soup = BeautifulSoup(urllib2.urlopen(url))

        song_list = soup.find(id="songlist")
        anchors = song_list.find_all("a")
        song_map = {}

        for anchor in anchors:
            href = anchor.get("href")
            if href and "mp3" in href:
                href = self.BASE_URL + href
                if href not in song_map:
                    song_map[href] = anchor.string

        return song_map

    def download_songs(self, song_map, dir_name):
        downloaded_mp3s = {}

        for href, song_name in song_map.items():
            link_soup = BeautifulSoup(urllib2.urlopen(href))
            audio = link_soup.find("audio")
            mp3_url = audio.get("src")
            if mp3_url not in downloaded_mp3s:
                downloaded_mp3s[mp3_url] = True
                file_name = sanitize_filename(song_name + ".mp3")

                mp3file = urllib2.urlopen(mp3_url)

                meta = mp3file.info()
                file_size = float(meta.get("Content-Length")) / 1000000

                file_on_disk_path = dir_name + "/" + file_name
                file_already_downloaded = False

                if os.path.exists(file_on_disk_path):
                    stat = os.stat(file_on_disk_path)
                    file_already_downloaded = round(
                        float(stat.st_size) / 1000000, 2
                    ) == round(file_size, 2)

                if not file_already_downloaded:
                    self.ui.update_log(
                        "[downloading] " + file_name + " [%.2f" % file_size + "MB]"
                    )

                    with open(file_on_disk_path, "wb") as output:
                        output.write(mp3file.read())
                        self.ui.update_log('[done] "' + file_name + '"')
                else:
                    self.ui.update_log(
                        '[skipping] "' + file_name + '"" already downloaded.'
                    )

    def fetch_from_url(self, url, download_dir):
        if not self.validate_url(url):
            self.ui.update_log("ERROR: Invalid url: " + url)
            return
        self.ui.update_log("INFO: Url found: " + url)

        dir_name = self.create_directories(url, download_dir)

        self.ui.update_log("INFO: crawling for links...")

        song_map = self.extract_song_links(url)

        if not song_map:
            self.ui.update_log(
                "ERROR: No links found for the url. Double check that the url is correct and try again."
            )
            self.ui.update_log("ERROR: url: " + url)
            return

        self.ui.update_log("INFO: " + str(len(song_map)) + " links acquired")

        self.download_songs(song_map, dir_name)

    def start_download(self, urls: list[str], download_dir: str):
        if urls is not None and len(urls) > 0:
            for url in urls:
                self.fetch_from_url(url, download_dir)
