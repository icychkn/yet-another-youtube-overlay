from bs4 import BeautifulSoup
from requests_html import HTMLSession
from youtube_dl import YoutubeDL


options = {
    'quiet': True,
    'skip_download': True
}
ydl = YoutubeDL(options)
ydl.add_default_info_extractors()


session = HTMLSession()
session.browser


def get_soup(url):
    response = session.get(url)
    response.html.render(keep_page = True)

    return BeautifulSoup(response.html.html, 'html.parser')


from app.youtube import channel
from app.youtube import watch
from app.youtube import playlist
