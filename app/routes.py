from app import app, debug_message
from flask import redirect, render_template, request, url_for
import os

import app.handler as handler


# homepage
# atm it only contains links to channels listed in the followed directory
@app.route('/')
def index():
    # creates a list in the format of:
    # [ {'info': <channel_a_info>, 'youtube_id': <channel_a_id>}, {'info': <channel_b_info>, 'youtube_id': <channel_b_info'} ...]
    # for every channel previously followed
    followed_channels = [{'info': handler.get_channel_info(x), 'youtube_id': x} for x in handler.get_followed()]

    return render_template('index.html', followed_channels = followed_channels)


# overlay for youtu.be
@app.route('/<string:youtube_id>')
def direct(youtube_id : str):
    if youtube_id == 'favicon.ico':
        abort(404)
    video = handler.get_video(youtube_id)

    return render_template('embed.html', video = video)


# overlay for youtube.com/embed/<video_id>
@app.route('/embed/<string:youtube_id>')
def embed(youtube_id : str):
    video = handler.get_video(youtube_id)

    return render_template('embed.html', video = video)


# overlay for youtube.com/watch?v=<video_id>
@app.route('/watch')
def watch():
    # guess what this does
    video_id = request.args.get('v') or 'dQw4w9WgXcQ'

    video_info = handler.get_video(video_id)
    video_info['audio_only'] = [x for x in video_info['raw']['formats'] if x['format_id'] == '251'][0]

    playlist_id = request.args.get('list') or ''
    playlist_index = int(request.args.get('index') or 1)
    playlist_page = int((playlist_index - playlist_index % 20) / 20) + 1
    playlist_videos = []
    if playlist_id:
        playlist_videos = handler.get_playlist_videos(playlist_id, playlist_page)
    playlist_info = { 'youtube_id': playlist_id, 'current_index': playlist_index, 'current_page': playlist_page, 'videos': playlist_videos }

    return render_template('watch.html', video_info = video_info, playlist_info = playlist_info)


# overlay for youtube.com/channel/<channel_id>?page=<page or 1>
@app.route('/channel/<string:channel_id>')
def channel(channel_id):
    channel_info = handler.get_channel_info(channel_id)
    is_followed = handler.is_followed(channel_id)

    page = int(request.args.get('page') or 1)

    videos = handler.get_channel_videos(channel_id, page)

    return render_template('channel.html', channel_info = channel_info, videos = videos, current_page = page, is_followed = is_followed)


# overlay for youtube.com/playlist?list=<playlist_id>&page=<page or 1>
@app.route('/playlist')
def playlist():
    playlist_id = request.args.get('list')
    page = int(request.args.get('page') or 1)

    playlist_videos = handler.get_playlist_videos(playlist_id, page)

    playlist_info = {'youtube_id': playlist_id, 'current_page': page, 'videos': playlist_videos}

    return render_template('playlist.html', playlist_info = playlist_info)


# handles adding/removing channels to/from the followed directory
@app.route('/follow', methods = ['POST'])
def follow_channel():
    channel_id = request.args.get('channel_id')
    if request.args.get('follow') == "True":
        debug_message('following channel: {}'.format(channel_id))
        handler.add_followed(channel_id)
    else:
        debug_message('unfollowing channel: {}'.format(channel_id))
        handler.del_followed(channel_id)

    return redirect(url_for('channel', channel_id = channel_id))


# exports the list of subscriptions in a format newpipe can import
@app.route('/export_newpipe_subscription')
def export_newpipe_subscription():
    followed_channels = [{'info': handler.get_channel_info(x), 'youtube_id': x} for x in handler.get_followed()]

    return render_template('newpipe_subscription.json', followed_channels = followed_channels)
