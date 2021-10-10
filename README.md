# Yet Another Youtube Overlay
Yet Another Youtube Overlay is my attempt at a youtube overlay built with Flask based on the work by Yotter and Invidious.

I wanted to experiment with an overlay that doesn't rely on a dedicated database for storing data on followed channels. This
project uses nothing more complex than plaintext files storing JSON serialized data to store raw responses from requests to
Youtube.

(I have not done any testing of this in Windows so I cannot guarentee it will work without modification)

WARNING: This is NOT production ready, it is merely a personal project.

# What works
Watching videos<br>
Viewing channels<br>
Following channels<br>
Viewing playlists<br>
Downloading audio tracks of videos<br>
?Embedding videos into other pages? (Further testing required)<br>

# Dependencies
<pre>
python==3.9.6
bs4==0.0.1
Flask==1.1.2
Jinja2==2.11.2
requests==2.26.0  # can't remember if actually needed
requests-html==0.10.0
youtube-dl==2021.6.6
</pre>

# Basic Setup
Download the repository<br>
git clone https://github.com/icychkn/yet-another-youtube-overlay

Install required packages<br>
pip3 install -r requirements.txt

Run the program itself<br>
python3 run.py

By default it runs on localhost on port 5000, this can be changed inside run.py

# Site Structure
<pre>
/                    # homepage, shows links to followed channels
/watch               # overlay for youtube's watch page
/channel             # overlay for youtube's channel page, shows the channel playlist which contains all videos that were uploaded by them
/playlist            # overlay for youtube's playlist page
/follow              # only used within the site to add and remove channels from the followed list
</pre>

# How does it work?
To save on pinging Youtube's servers continuously every time a page is refreshed, it will cache channel info and playlist
pages.

The handler.py file handles retrieving data from either the cache or the internet depending on whether the file already
exists and isn't more than 24 hours old.

The routes.py file stores functions that is used by Flask to generate pages for the end user.

The "cache" directory stores responses from requests to Youtube for channels and playlists.

The "followed" directory is used to store empty files with names that correlate to channel ids as a method of tracking
followed channels.

The "static" directory atm contains nothing more than a css file used for styling the site.

The "templates" directory contains template html files used by Flask to show to the end user.

The "youtube" directory contains a few files from the Yotter project necessary to send sane requests to Youtube's site.

# More details on the cache
The cache uses the following directory structure to store data in

<pre>
cache/
  channel/
    &lt;channel 1 id&gt;/
    &lt;channel 2 id&gt;/
    ...
  playlist/
    &lt;playlist 1 id&gt;/
      1
      2
      ...
    ...
</pre>

Directories are created for each channel and playlist using their youtube id as the name under their respective types.

Atm, the only file stored under channel folders is the "info" file which stores all info on a channel, including it's title
and description

Playlist folders store files with integer names that correlate with pages that store 20 videos each, i.e. file "1"
contains the first 20 videos, file "2" contains the next 20 videos, and file "32" contains videos 620 - 640.

By default, when a playlist file is requested, it is first checked whether it was last modified over 24 hours ago. If
it is, it will be reacquired. This behavior can be bypassed to always use the cached files and only retrieving ones that
aren't cached by passing True to the force_cache keyword variable. However, this may result in strange behavior due to
how the playlist videos are ordered from newest to oldest.

Channel info files are never updated.

# Contributing
This is a personal project, so I can't promise I'll accept any changes being pushed to this repo.

Feel free to fork it and modify it however you want.

# License
None, feel free to do whatever you wish with this

