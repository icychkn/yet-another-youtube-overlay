from app.youtube import ydl
import app.youtube.video as video


def get_info(_id):
    base_watch_url = 'https://www.youtube.com/watch?v={}'
    info = ydl.extract_info(base_watch_url.format(_id), download = False)

    return {'video_id': info['id'], 'title': info['title'], 'description': info['description'], 'channel_title': info['uploader'], 'channel_id': info['channel_id'], 'video_url': video.get_best_url(info), 'raw': info}



