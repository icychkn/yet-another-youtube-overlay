# Taken from https://github.com/ytorg/Yotter

from app.youtube import proto
import base64
import json
import urllib


headers = {
    ('Accept', '*/*'),
    ('Accept-Language', 'en-US,en;q=0.5'),
    ('X-YouTube-Client-Name', '2'),
    ('X-YouTube-Client-Version', '2.20180614'),
}


def playlist_ctoken(playlist_id, offset):
    offset = proto.uint(1, offset)
    offset = b'PT:' + proto.unpadded_b64encode(offset)
    offset = proto.string(15, offset)

    continuation_info = proto.string(3, proto.percent_b64encode(offset))

    playlist_id = proto.string(2, 'VL' + playlist_id)
    pointless_nest = proto.string(80226972, playlist_id + continuation_info)

    return base64.urlsafe_b64encode(pointless_nest).decode('ascii')


def get_videos(playlist_id, page):
    url = 'https://m.youtube.com/playlist?ctoken=' + playlist_ctoken(playlist_id, (int(page)-1)*20) + '&pbj=1'
    headers = {
        'User-Agent': '  Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-YouTube-Client-Name': '2',
        'X-YouTube-Client-Version': '2.20180508'
    }

    request = urllib.request.Request(url)
    for k in headers:
        request.add_header(k, headers[k])

    content = urllib.request.urlopen(request).read()

    info = json.loads(content.decode('utf-8'))
    return info 


def get_all_videos(playlist_id):
    results = []
    i = 1
    response = get_videos(playlist_id, i)
    while 'continuationContents' in response['response']:
        current_videos = response['response']['continuationContents']['playlistVideoListContinuation']['contents']
        for vid in current_videos:
            results.append(vid['playlistVideoRenderer']['videoId'])
        i += 1
        response = get_videos(playlist_id, i)
    return results

