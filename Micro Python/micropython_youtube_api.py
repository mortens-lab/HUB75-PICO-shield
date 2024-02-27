# The MIT License (MIT)
#
# Copyright (c) 2019 Seon "Unexpected Maker" Rozenblum
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`micropython_youtube_api` - YouTube API 
====================================================
See examples folder for how to use
* Author(s): Seon Rozenblum
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/unexpectedmaker/micropython-youtube-api"

import urequests as ureq
import json, time

class YoutubeAPI:

    def __init__(self, channel_id, app_key_id, query_interval_sec=60):
        if not isinstance(channel_id, str):
            raise TypeError("'channel_id' must be provided")
        self.channel_id = channel_id
        if not isinstance(app_key_id, str):
            raise TypeError("'app_key_id' must be provided")
        self.app_key_id = app_key_id
        if not isinstance(query_interval_sec, int):
            raise TypeError("'query_interval_sec' must be an int")
        self.query_interval_sec = query_interval_sec
        self._update_stats_time = time.time() - 10

        # cached stat data
        self._subs = 0
        self._views = 0
        self._comments = 0
        self._videos = 0

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    # Update the stats is the correct time interval has passed
    def _update_stats(self):
        if self._update_stats_time < time.time():
            self._grab_stats()
            self._update_stats_time = time.time() + self.query_interval_sec

    def _grab_stats(self):
        # Create the API query to send to GoogleAPI
        urlbase = "https://www.googleapis.com/youtube/v3/channels"
        youtube_url = "{}?part=statistics&id={}&key={}".format(urlbase, self.channel_id, self.app_key_id )

        #print ("Contacting GoogleAPI... " )

        # request the data from Google
        req = ureq.get(youtube_url)
        if req.status_code == 200:
            stats = [{
                    'subs': stat['statistics']['subscriberCount'], 
                    'views': stat['statistics']['viewCount'],
                    'videos': stat['statistics']['videoCount'],
                    'comments': stat['statistics']['commentCount']
                    } for stat in req.json()['items']]
                
            # for stat in YoutubeApi.stats
            self._subs = stats[0]['subs']
            self._views = stats[0]['views']
            self._videos = stats[0]['videos']
            self._comments = stats[0]['comments']         
        else:
            print( "ERROR: status_code: " + str(req.status_code) )
        req.close()
    
    # Accessorss for each of the stats returned by the API
    @property
    def subs(self):
        self._update_stats()
        return self._subs

    @property
    def views(self):
        self._update_stats()
        return self._views

    @property
    def videos(self):
        self._update_stats()
        return self._videos

    @property
    def comments(self):
        self._update_stats()
        return self._comments
