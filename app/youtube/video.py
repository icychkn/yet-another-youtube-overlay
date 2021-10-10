def get_best_url(info):
    formats = [_format for _format in info['formats'] if _format['vcodec'] != 'none' and _format['acodec'] != 'none' and _format['format_note'] != '144p']

    video_url = formats[0]['url']
    return video_url
