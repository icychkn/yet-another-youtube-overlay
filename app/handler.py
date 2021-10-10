from app import debug_message

from pathlib import Path
import json
import os
import time

import app.youtube as yt

dir_followed = 'app/followed'
dir_cache    = 'app/cache'


# adds file <channel_id> under followed directory
def add_followed(channel_id : str):
    debug_message("ADD_FOLLOWED: {}".format(channel_id))
    Path('{}/{}'.format(dir_followed, channel_id)).touch()


# deletes file <channel_id> under followed directory
def del_followed(channel_id : str):
    debug_message("DEL_FOLLOWED: {}".format(channel_id))
    os.remove('{}/{}'.format(dir_followed, channel_id))


# returns true if file <channel_id> exists under followed directory, else false
def is_followed(channel_id : str):
    debug_message("IS_FOLLOWED: {}".format(channel_id))
    return os.path.exists('{}/{}'.format(dir_followed, channel_id))


# returns list of filenames under the followed directory
def get_followed():
    debug_message("GET_FOLLOWED")
    return os.listdir(dir_followed)


# creates a directory under the cache directory if it doesn't exist
def add_dir_to_cache(dirname : str):
    if not os.path.exists('{}/{}'.format(dir_cache, dirname)):
        Path('{}/{}'.format(dir_cache, dirname)).mkdir(parents = True)


# returns true if file at path is under cache directory, else false
def is_file_in_cache(path : str):
    return os.path.exists('{}/{}'.format(dir_cache, path))


# writes data to the file at path under the cache directory
def write_file_to_cache(path : str, data):
    file = open('{}/{}'.format(dir_cache, path), 'w')
    file.write(json.dumps(data))
    file.close()


# reads file under cache at <path>
def read_file_from_cache(path : str):
    file = open('{}/{}'.format(dir_cache, path), 'r')

    data = []
    try:
        data = json.loads(file.read())
    except:
        pass
    file.close()

    return data

# channel wrapper for add_dir_to_cache
# creates a directory under the "channel" directory in the cache with name <channel_id>
# equivalent to: mkdir <cache dir>/channel/<channel_id>
def add_channel_to_cache(channel_id : str):
    debug_message("ADD_CHANNEL_TO_CACHE: {}".format(channel_id))
    add_dir_to_cache('channel/{}'.format(channel_id))


# channel wrapper for write_file_to_cache
# (over)writes data to a file in the cache after serializing it to json
# equivalent to: echo json_data > <cache dir>/<channel id>/<filename>
# where json_data is data serialized to json
def write_file_to_channel_cache(channel_id : str, filename : str, data = []):
    write_file_to_cache('channel/{}/{}'.format(channel_id, filename), data)


# channel wrapper for is_file_in_cache
# returns true if <filename> exists in channel cache under directory <channel_id>
def is_file_in_channel_cache(channel_id : str, filename : str):
    return is_file_in_cache('channel/{}/{}'.format(channel_id, filename))


# channel wrapper for read_file_from_cache
# reads file from <cache dir>/channel/<channel_id>/<filename>
def read_file_from_channel_cache(channel_id : str, filename : str):
    return read_file_from_cache('channel/{}/{}'.format(channel_id, filename))


# playlist wrapper for add_dir_to_cache
# creates dir at <cache dir>/playlist/<playlist_id>
def add_playlist_to_cache(playlist_id : str):
    add_dir_to_cache('playlist/{}'.format(playlist_id))


# playlist wrapper for write_file_to_cache
# saves data to <cache dir>/playlist/<playlist_id>/<filename>
def write_file_to_playlist_cache(playlist_id : str, filename : str, data = []):
    write_file_to_cache('playlist/{}/{}'.format(playlist_id, filename), data)


# playlist wrapper for is_file_in_cache
# checks for file at <cache dir>/playlist/<playlist_id>/<filename>
def is_file_in_playlist_cache(playlist_id : str, filename : str):
    return is_file_in_cache('playlist/{}/{}'.format(playlist_id, filename))


# playlist wrapper for read_file_from_cache
# reads file from <cache dir>/playlist/<playlist_id>/<filename>
def read_file_from_playlist_cache(playlist_id : str, filename : str):
    return read_file_from_cache('playlist/{}/{}'.format(playlist_id, filename))


# handles retrieving channel info from either cache or the internet
def get_channel_info(channel_id : str):
    add_channel_to_cache(channel_id)

    channel_info = []
    # if file was cached before, use it
    if is_file_in_channel_cache(channel_id, 'info'):
        channel_info = read_file_from_channel_cache(channel_id, 'info')
    # otherwise retrieve from the internet and cache it
    else:
        channel_info = yt.channel.get_info(channel_id)
        # saves channel_info to file at <cache dir>/channel/<channel_id>/info
        write_file_to_channel_cache(channel_id, 'info', data = channel_info)

    return channel_info


# wrapper for yt.watch.get_info which retrieves all info on a video
def get_video(video_id : str):
    return yt.watch.get_info(video_id)


# handles retrieving playlists from either cache or the internet
def get_playlist_videos(playlist_id : str, page : int, prefer_cache = True, force_cache = False):
    add_playlist_to_cache(playlist_id)

    # reason for testing force_cache first is if it's true, then it will execute without
    # testing anything else, saves a bit of processing power

    # if force_cache
    # or file is already cached
    # and cache is preferred
    # and cached file is no longer than a day old
    # then use cache
    if force_cache or is_file_in_playlist_cache(playlist_id, page) and prefer_cache and not time.time() > 86400 + os.path.getctime('{}/playlist/{}/{}'.format(dir_cache, playlist_id, page)):
        debug_message("reading file from playlist cache: {}/{}".format(playlist_id, page))
        videos = read_file_from_playlist_cache(playlist_id, page)
    # else update cache
    else:
        debug_message("updating file in playlist cache: {}/{}".format(playlist_id, page))
        videos = yt.playlist.get_videos(playlist_id, page)

        # saves videos to file at <cache dir>/playlist/<playlist_id>/<page>
        write_file_to_playlist_cache(playlist_id, page, data = videos)

    return videos


# wrapper for get_playlist_videos that gets the channel playlist
# the channel playlist contains every video the channel uploaded
def get_channel_videos(channel_id : str, page : int, prefer_cache = True, force_cache = False):
    return get_playlist_videos('UU{}'.format(channel_id[2:]), page, prefer_cache, force_cache)

