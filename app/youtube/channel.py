from app.youtube import ydl, get_soup
import feedparser


base_channel_url            = 'https://www.youtube.com/channel/{}/about'
base_channel_feed           = 'https://www.youtube.com/feeds/videos.xml?channel_id={}'


def get_info(channel_id):
    soup = get_soup(base_channel_url.format(channel_id))

    channel_title = soup.find('yt-formatted-string', class_ = 'style-scope ytd-channel-name').text
    description = soup.find('yt-formatted-string', class_ = 'style-scope ytd-channel-about-metadata-renderer').text

    return { 'title': channel_title, 'youtube_id': channel_id, 'description': description, 'videos': []}


def get_feed(channel_id):
    feed = feedparser.parse(base_channel_feed.format(channel_id))

    return [{'video_id': x['yt_videoid'], 'video_title': x['title'], 'video_url': x['link'].split('.com')[1], 'channel_title': x['author'], 'channel_url': x['author_detail']['href'], 'published': x['published'], 'thumbnail_url': x['media_thumbnail'][0]['url']} for x in feed.entries]


def get_multiple_feeds(channel_ids):
    latest_videos = []

    for x in channel_ids:
        latest_videos += get_feed(x)
    sorted_videos = [x for x in reversed(sorted(latest_videos, key = lambda k: k['published']))]

    return sorted_videos

