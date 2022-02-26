from bs4 import BeautifulSoup
from requests_html import HTMLSession
from youtube_dl import YoutubeDL


options = {
    'quiet': True,
    'skip_download': True
}
ydl = YoutubeDL(options)
ydl.add_default_info_extractors()


def get_soup(url):
    session = HTMLSession()
    session.browser

    response = session.get(url)
    response.html.render(keep_page = True)

    session.close()

    return BeautifulSoup(response.html.html, 'html.parser')


from app.youtube import channel
from app.youtube import watch
from app.youtube import playlist
