# -*- coding: utf-8 -*-

'''
    Genesis XBMC Addon
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers
from metahandler import metacontainers


action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
movieLibrary        = os.path.join(xbmc.translatePath(getSetting("movie_library")),'')
tvLibrary           = os.path.join(xbmc.translatePath(getSetting("tv_library")),'')
PseudoTV            = xbmcgui.Window(10000).getProperty('PseudoTVRunning')
addonLogos          = os.path.join(addonPath,'resources/logos')
favData             = os.path.join(dataPath,'favourite_movies.list')
favData2            = os.path.join(dataPath,'favourite_tv.list')
viewData            = os.path.join(dataPath,'views.list')
offData             = os.path.join(dataPath,'offset.list')


class main:
    def __init__(self):
        global action
        index().container_art()
        index().container_data()
        index().settings_reset()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        source = urllib.unquote_plus(params["source"])
        except:     source = None
        try:        provider = urllib.unquote_plus(params["provider"])
        except:     provider = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        tvdb = urllib.unquote_plus(params["tvdb"])
        except:     tvdb = None
        try:        tvrage = urllib.unquote_plus(params["tvrage"])
        except:     tvrage = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        show_alt = urllib.unquote_plus(params["show_alt"])
        except:     show_alt = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None

        if action == None:                            root().get()
        elif action == 'root_movies':                 root().movies()
        elif action == 'root_shows':                  root().shows()
        elif action == 'root_genesis':                root().genesis()
        elif action == 'root_tools':                  root().tools()
        elif action == 'root_search':                 root().search()
        elif action == 'item_queue':                  contextMenu().item_queue()
        elif action == 'view_movies':                 contextMenu().view('movies')
        elif action == 'view_tvshows':                contextMenu().view('tvshows')
        elif action == 'view_seasons':                contextMenu().view('seasons')
        elif action == 'view_episodes':               contextMenu().view('episodes')
        elif action == 'cache_clear':                 contextMenu().cache_clear()
        elif action == 'playlist_open':               contextMenu().playlist_open()
        elif action == 'settings_open':               contextMenu().settings_open()
        elif action == 'settings_urlresolver':        contextMenu().settings_open('script.module.urlresolver')
        elif action == 'settings_metahandler':        contextMenu().settings_open('script.module.metahandler')
        elif action == 'favourite_movie_add':         contextMenu().favourite_add(favData, name, url, image, imdb, year, refresh=True)
        elif action == 'favourite_movie_from_search': contextMenu().favourite_add(favData, name, url, image, imdb, year)
        elif action == 'favourite_movie_delete':      contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_tv_add':            contextMenu().favourite_add(favData2, name, url, image, imdb, year, refresh=True)
        elif action == 'favourite_tv_from_search':    contextMenu().favourite_add(favData2, name, url, image, imdb, year)
        elif action == 'favourite_tv_delete':         contextMenu().favourite_delete(favData2, name, url)
        elif action == 'trakt_manager':               contextMenu().trakt_manager('movie', name, imdb)
        elif action == 'trakt_tv_manager':            contextMenu().trakt_manager('show', name, imdb)
        elif action == 'metadata_movies':             contextMenu().metadata('movie', imdb, '', '')
        elif action == 'metadata_tvshows':            contextMenu().metadata('tvshow', imdb, '', '')
        elif action == 'metadata_seasons':            contextMenu().metadata('season', imdb, season, '')
        elif action == 'metadata_episodes':           contextMenu().metadata('episode', imdb, season, episode)
        elif action == 'playcount_movies':            contextMenu().playcount('movie', imdb, '', '')
        elif action == 'playcount_episodes':          contextMenu().playcount('episode', imdb, season, episode)
        elif action == 'library_movie_add':           contextMenu().library_movie_add(name, title, year, imdb, url)
        elif action == 'library_movie_list':          contextMenu().library_movie_list(url)
        elif action == 'library_tv_add':              contextMenu().library_tv_add(name, year, imdb, url)
        elif action == 'library_tv_list':             contextMenu().library_tv_list(url)
        elif action == 'library_update':              contextMenu().library_update()
        elif action == 'library_service':             contextMenu().library_update(silent=True)
        elif action == 'library_trakt_collection':    contextMenu().library_preset_list('trakt_collection')
        elif action == 'library_trakt_watchlist':     contextMenu().library_preset_list('trakt_watchlist')
        elif action == 'library_imdb_watchlist':      contextMenu().library_preset_list('imdb_watchlist')
        elif action == 'library_tv_trakt_collection': contextMenu().library_preset_list('trakt_tv_collection')
        elif action == 'library_tv_trakt_watchlist':  contextMenu().library_preset_list('trakt_tv_watchlist')
        elif action == 'library_tv_imdb_watchlist':   contextMenu().library_preset_list('imdb_tv_watchlist')
        elif action == 'toggle_movie_playback':       contextMenu().toggle_playback('movie', name, title, year, imdb, '', '', '', '', '', '', '', '')
        elif action == 'toggle_episode_playback':     contextMenu().toggle_playback('episode', name, title, year, imdb, tvdb, tvrage, season, episode, show, show_alt, date, genre)
        elif action == 'download':                    contextMenu().download(name, url, provider)
        elif action == 'trailer':                     contextMenu().trailer(name, url)
        elif action == 'shows_favourites':            favourites().shows()
        elif action == 'movies_favourites':           favourites().movies()
        elif action == 'movies':                      movies().get(url)
        elif action == 'movies_userlist':             movies().get(url)
        elif action == 'movies_popular':              movies().popular()
        elif action == 'movies_boxoffice':            movies().boxoffice()
        elif action == 'movies_views':                movies().views()
        elif action == 'movies_oscars':               movies().oscars()
        elif action == 'movies_added':                movies().added()
        elif action == 'movies_trending':             movies().trending()
        elif action == 'movies_trakt_collection':     movies().trakt_collection()
        elif action == 'movies_trakt_watchlist':      movies().trakt_watchlist()
        elif action == 'movies_imdb_watchlist':       movies().imdb_watchlist()
        elif action == 'movies_search':               movies().search(query)
        elif action == 'shows':                       shows().get(url)
        elif action == 'shows_userlist':              shows().get(url)
        elif action == 'shows_popular':               shows().popular()
        elif action == 'shows_rating':                shows().rating()
        elif action == 'shows_views':                 shows().views()
        elif action == 'shows_active':                shows().active()
        elif action == 'shows_trending':              shows().trending()
        elif action == 'shows_trakt_collection':      shows().trakt_collection()
        elif action == 'shows_trakt_watchlist':       shows().trakt_watchlist()
        elif action == 'shows_imdb_watchlist':        shows().imdb_watchlist()
        elif action == 'shows_search':                shows().search(query)
        elif action == 'seasons':                     seasons().get(url, year, imdb, image, genre, plot, show)
        elif action == 'episodes':                    episodes().get(name, url, year, imdb, tvdb, image, genre, plot, show, show_alt)
        elif action == 'episodes2':                   episodes().get2(url)
        elif action == 'episodes_added':              episodes().added()
        elif action == 'episodes_calendar':           episodes().calendar(url)
        elif action == 'actors_movies':               actors().movies(query)
        elif action == 'actors_shows':                actors().shows(query)
        elif action == 'genres_movies':               genres().movies()
        elif action == 'genres_shows':                genres().shows()
        elif action == 'years_movies':                years().movies()
        elif action == 'calendar_episodes':           calendar().episodes()
        elif action == 'channels_movies':             channels().movies()
        elif action == 'userlists_movies':            userlists().movies()
        elif action == 'userlists_shows':             userlists().shows()
        elif action == 'get_host':                    resolver().get_host(name, title, year, imdb, url, image, genre, plot, tvdb, tvrage, date, show, show_alt, season, episode)
        elif action == 'play_moviehost':              resolver().play_host('movie', name, url, imdb, source, provider)
        elif action == 'play_tvhost':                 resolver().play_host('episode', name, url, imdb, source, provider)
        elif action == 'play':                        resolver().run(name, title, year, imdb, tvdb, tvrage, season, episode, show, show_alt, date, genre, url)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, content, name, url, imdb='0'):
        self.video_info(content, name, imdb)

        if self.folderPath.startswith(sys.argv[0]) or PseudoTV == 'True':
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                if self.content == 'movie':
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "genre", "year", "rating", "director", "trailer", "tagline", "plot", "plotoutline", "originaltitle", "writer", "studio", "mpaa", "country", "runtime", "votes", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)
                    meta = meta['result']['movies']
                    self.meta = [i for i in meta if i['file'].endswith(self.file)][0]
                    meta = {'title': self.meta['title'], 'originaltitle': self.meta['originaltitle'], 'year': self.meta['year'], 'genre': str(self.meta['genre']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'country': str(self.meta['country']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'votes': self.meta['votes'], 'mpaa': self.meta['mpaa'], 'duration': self.meta['runtime'], 'trailer': self.meta['trailer'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'studio': str(self.meta['studio']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'tagline': self.meta['tagline'], 'plotoutline': self.meta['plotoutline'], 'plot': self.meta['plot']}

                elif self.content == 'episode':
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "plot", "rating", "writer", "firstaired", "runtime", "director", "season", "episode", "showtitle", "thumbnail", "file"]}, "id": 1}' % (self.season, self.episode))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)
                    meta = meta['result']['episodes']
                    self.meta = [i for i in meta if i['file'].endswith(self.file)][0]
                    meta = {'title': self.meta['title'], 'tvshowtitle': self.meta['showtitle'], 'season': self.meta['season'], 'episode': self.meta['episode'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'duration': self.meta['runtime'], 'premiered': self.meta['firstaired'], 'plot': self.meta['plot']}

                poster = self.meta['thumbnail']
            except:
                meta = {'label': self.name, 'title': self.name}
                poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(0, 250):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, content, name, imdb):
        self.name = name
        self.content = content
        self.file = self.name + '.strm'
        self.file = self.file.translate(None, '\/:*?"<>|').strip('.')

        if self.content == 'movie':
            self.title = self.name.rsplit(' (', 1)[0].strip()
            self.year = '%04d' % int(self.name.rsplit(' (', 1)[-1].split(')')[0])
            if imdb == '0': imdb = metaget.get_meta('movie', self.title ,year=str(self.year))['imdb_id']
            self.imdb = re.sub('[^0-9]', '', imdb)
            self.subtitle = subtitles().get(self.name, self.imdb, '', '')

        elif self.content == 'episode':
            self.show = self.name.rsplit(' ', 1)[0]
            if imdb == '0': imdb = metaget.get_meta('tvshow', self.show)['imdb_id']
            self.imdb = re.sub('[^0-9]', '', imdb)
            self.season = '%01d' % int(name.rsplit(' ', 1)[-1].split('S')[-1].split('E')[0])
            self.episode = '%01d' % int(name.rsplit(' ', 1)[-1].split('E')[-1])
            self.subtitle = subtitles().get(self.name, self.imdb, self.season, self.episode)

    def offset_add(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"' % (self.name, self.imdb, self.currentTime))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_delete(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (self.name, self.imdb) in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(offData, 'w')
            file.write(str(write))
            file.close()
        except:
            return

    def offset_read(self):
        try:
            self.offset = '0'
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            read = [i for i in read.splitlines(True) if '"%s"|"%s"|"' % (self.name, self.imdb) in i][0]
            self.offset = re.compile('".+?"[|]".+?"[|]"(.+?)"').findall(read)[0]
        except:
            return

    def change_watched(self):
        if self.content == 'movie':
            if getSetting("watched_sync") == 'true':
                try:
                    metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)
                except:
                    pass
                try:
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)
                    meta = meta['result']['movies']
                    meta = [i for i in meta if i['file'].endswith(self.file)][0]
                    while xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]) or xbmc.getInfoLabel('Container.FolderPath') == '': xbmc.sleep(1000)
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(meta['movieid']))
                except:
                    pass
            else:
                try:
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['movieid']))
                except:
                    metaget.change_watched(self.content, '', self.imdb, season='', episode='', year='', watched=7)

        elif self.content == 'episode':
            if getSetting("watched_sync") == 'true':
                try:
                    metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)
                except:
                    pass
                try:
                    meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"]}, "id": 1}' % (self.season, self.episode))
                    meta = unicode(meta, 'utf-8', errors='ignore')
                    meta = json.loads(meta)
                    meta = meta['result']['episodes']
                    meta = [i for i in meta if i['file'].endswith(self.file)][0]
                    while xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]) or xbmc.getInfoLabel('Container.FolderPath') == '': xbmc.sleep(1000)
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(meta['episodeid']))
                except:
                    pass
            else:
                try:
                    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['episodeid']))
                except:
                    metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)

    def resume_playback(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30354).encode("utf-8"), offset_time), '', self.name, language(30355).encode("utf-8"), language(30356).encode("utf-8"))
        if yes: self.seekTime(offset)

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if PseudoTV == 'True': return

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30315).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.offset_read()
            self.resume_playback()

    def onPlayBackEnded(self):
        if PseudoTV == 'True': return
        self.offset_delete()
        self.change_watched()

    def onPlayBackStopped(self):
        if PseudoTV == 'True': return
        self.offset_delete()
        self.offset_add()
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            if not (season == '' or episode == ''): result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb, 'season': season, 'episode': episode}])['data']
            else: result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
        for lang in langs.split(','):
            filter = [i for i in result if lang == i['SubLanguageID']]
            if filter == []: continue
            for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
            subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
            try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
            except: pass
            break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30313).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin('Container.Refresh')

    def container_art(self):
        global addonArt
        global addonIcon
        global addonFanart
        addonArt = os.path.join(addonPath,'resources/art')
        addonArt = os.path.join(addonArt,getSetting("appearance").lower().replace(' ', ''))
        addonIcon = os.path.join(addonArt,'icon.png')
        addonFanart = os.path.join(addonArt,'fanart.jpg')
        if getSetting("appearance") == '-':
            addonIcon = os.path.join(addonPath,'icon.png')
            addonFanart = ''

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(favData2):
            file = xbmcvfs.File(favData2, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(offData):
            file = xbmcvfs.File(offData, 'w')
            file.write('')
            file.close()

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def settings_reset(self):
        try:
            if getSetting("settings_version") == '1.0.0': return
            setSetting('settings_version', '1.0.0')
        except:
            return

    def rootList(self, rootList):
        total = len(rootList)

        cacheToDisc = False
        if action == 'actors_movies' or action == 'actors_shows': cacheToDisc = True

        for i in rootList:
            try:
                try: name = language(i['name']).encode("utf-8")
                except: name = i['name']

                root = i['action']
                u = '%s?action=%s' % (sys.argv[0], root)
                try: u += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                if root == 'folder_downloads':
                    u = xbmc.translatePath(getSetting("downloads"))
                elif root == 'folder_movie':
                    u = movieLibrary
                elif root == 'folder_tv':
                    u = tvLibrary

                if u == '': raise Exception()

                if i['image'].startswith('http://'):
                    image = i['image']
                elif getSetting("appearance") == '-':
                    if root == 'episodes_added': image = 'DefaultRecentlyAddedEpisodes.png'
                    elif root == 'movies_added': image = 'DefaultRecentlyAddedMovies.png'
                    elif root == 'root_genesis': image = 'DefaultVideoPlaylists.png'
                    elif root == 'root_tools': image = 'DefaultAddonProgram.png'
                    elif root.startswith('movies') or root.endswith('_movies'): image = 'DefaultMovies.png'
                    elif root.startswith('episodes') or root.endswith('_episodes'): image = 'DefaultTVShows.png'
                    elif root.startswith('shows') or root.endswith('_shows'): image = 'DefaultTVShows.png'
                    else: image = 'DefaultFolder.png'
                else:
                    image = '%s/%s' % (addonArt, i['image'])

                cm = []
                replaceItems = False
                if root == 'movies_userlist':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_movie_list&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
                elif root == 'shows_userlist':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_tv_list&url=%s)' % (sys.argv[0], urllib.quote_plus(i['url']))))
                elif root == 'movies_trakt_collection':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_trakt_collection)' % (sys.argv[0])))
                elif root == 'movies_trakt_watchlist':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_trakt_watchlist)' % (sys.argv[0])))
                elif root == 'movies_imdb_watchlist':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_imdb_watchlist)' % (sys.argv[0])))
                elif root == 'shows_trakt_collection':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_tv_trakt_collection)' % (sys.argv[0])))
                elif root == 'shows_trakt_watchlist':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_tv_trakt_watchlist)' % (sys.argv[0])))
                elif root == 'shows_imdb_watchlist':
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_tv_imdb_watchlist)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=library_update)' % (sys.argv[0])))
                if root == 'movies_search' or root == 'shows_search' or root == 'actors_movies' or root == 'actors_shows':
                    cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    replaceItems = True

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=replaceItems)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)

    def channelList(self, channelList):
        if channelList == None: return

        total = len(channelList)
        for i in channelList:
            try:
                channel, title, year, imdb, genre, plot = i['name'], i['title'], i['year'], i['imdb'], i['genre'], i['plot']
                image = '%s/%s.png' % (addonLogos, channel)
                name = '%s (%s)' % (title, year)
                label = "[B]%s[/B] : %s" % (channel.upper(), name)
                if plot == '0': plot = addonDesc

                sysname, sysurl, sysimage, systitle, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(name), urllib.quote_plus(image), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if not getSetting("autoplay") == 'false':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&image=%s&genre=%s&plot=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysimage, sysgenre, sysplot, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = True

                meta = {'Label': title, 'Title': title, 'Studio': channel, 'Duration': '1440', 'Plot': plot}

                cm = []
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=toggle_movie_playback&name=%s&title=%s&imdb=%s&year=%s)' % (sys.argv[0], sysname, systitle, sysimdb, sysyear)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)

    def movieList(self, movieList):
        if movieList == None: return

        autoplay = getSetting("autoplay")
        if PseudoTV == 'True': autoplay = 'true'

        cacheToDisc = False
        if action == 'movies_search': cacheToDisc = True

        getmeta = getSetting("meta")
        if action == 'movies_search': getmeta = ''

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        total = len(movieList)
        for i in movieList:
            try:
                name, title, year, imdb, url, image, genre, plot = i['name'], i['title'], i['year'], i['imdb'], i['url'], i['image'], i['genre'], i['plot']
                if plot == '0': plot = addonDesc

                sysname, systitle, sysyear, sysimdb, sysurl, sysimage, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot)

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&image=%s&genre=%s&plot=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysimage, sysgenre, sysplot)
                    isFolder = True

                if getmeta == 'true':
                    meta = metaget.get_meta('movie', title ,year=year)
                    playcountMenu = language(30403).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30404).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                    if trailer == '': trailer = sysurl
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    trailer, poster = sysurl, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=toggle_movie_playback&name=%s&title=%s&year=%s&imdb=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                if getmeta == 'true' and not action == 'movies_search':
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=trakt_manager&name=%s&imdb=%s)' % (sys.argv[0], sysname, sysimdb)))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_movie_add&name=%s&title=%s&year=%s&imdb=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)))
                if action == 'movies_favourites':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_delete&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], systitle, sysimdb, sysurl, sysimage, sysyear)))
                else:
                    if not '"%s"' % url in favRead: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], systitle, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_movie_delete&name=%s&url=%s)' % (sys.argv[0], systitle, sysurl)))
                cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        try:
            next = movieList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30361).encode("utf-8"), next, os.path.join(addonArt,'item_next.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=movies&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(movies)'):
                return index().container_view('movies', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def showList(self, showList):
        if showList == None: return

        getmeta = getSetting("meta")
        if action == 'shows_search': getmeta = ''

        file = xbmcvfs.File(favData2)
        favRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                name, title, year, imdb, url, image, genre, plot = i['name'], i['name'], i['year'], i['imdb'], i['url'], i['image'], i['genre'], i['plot']
                if plot == '0': plot = addonDesc

                sysname, systitle, sysyear, sysimdb, sysurl, sysimage, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot)

                u = '%s?action=seasons&url=%s&year=%s&imdb=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysyear, sysimdb, sysimage, sysgenre, sysplot, sysname)

                if getmeta == 'true':
                    meta = metaget.get_meta('tvshow', title, imdb_id=imdb)
                    meta.update({'playcount': 0, 'overlay': 0})
                    playcountMenu = language(30403).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30404).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    poster, banner = meta['cover_url'], meta['banner_url']
                    if banner == '': banner = poster
                    if banner == '': banner = image
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': title, 'year' : year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    poster, banner = image, image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                meta.update({'art(banner)': banner, 'art(poster)': poster})

                cm = []
                cm.append((language(30415).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], sysname)))
                if getmeta == 'true' and not action == 'shows_search':
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                if not (getSetting("trakt_user") == '' or getSetting("trakt_password") == ''):
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=trakt_tv_manager&name=%s&imdb=%s)' % (sys.argv[0], sysname, sysimdb)))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=library_tv_add&name=%s&year=%s&imdb=%s&url=%s)' % (sys.argv[0], sysname, sysyear, sysimdb, sysurl)))
                if action == 'shows_favourites':
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl))) 
                elif action.startswith('shows_search'):
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                else:
                    if not '"%s"' % url in favRead: cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=favourite_tv_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                if action == 'shows_search':
                    if '"%s"' % url in favRead: suffix = '[B][F][/B] '
                    else: suffix = ''
                    name = suffix + name

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        try:
            next = showList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30361).encode("utf-8"), next, os.path.join(addonArt,'item_next.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=shows&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(tvshows)'):
                return index().container_view('tvshows', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def seasonList(self, seasonList):
        if seasonList == None: return

        try:
            year, imdb, tvdb, genre, plot, show, show_alt = seasonList[0]['year'], seasonList[0]['imdb'], seasonList[0]['tvdb'], seasonList[0]['genre'], seasonList[0]['plot'], seasonList[0]['show'], seasonList[0]['show_alt']
            if plot == '0': plot = addonDesc

            if getSetting("meta") == 'true':
                seasons = []
                for i in seasonList: seasons.append(i['season'])
                season_meta = metaget.get_seasons(show, imdb, seasons)
                meta = metaget.get_meta('tvshow', show, imdb_id=imdb)
                banner = meta['banner_url']
            else:
                meta = {'tvshowtitle': show, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                banner = ''
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(seasonList)
        for i in range(0, int(total)):
            try:
                name, url, image = seasonList[i]['name'], seasonList[i]['url'], seasonList[i]['image']
                sysname, sysurl, sysimage, sysyear, sysimdb, systvdb, sysgenre, sysplot, sysshow, sysshow_alt = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show), urllib.quote_plus(show_alt)
                u = '%s?action=episodes&name=%s&url=%s&year=%s&imdb=%s&tvdb=%s&image=%s&genre=%s&plot=%s&show=%s&show_alt=%s' % (sys.argv[0], sysname, sysurl, sysyear, sysimdb, systvdb, sysimage, sysgenre, sysplot, sysshow, sysshow_alt)

                if getSetting("meta") == 'true':
                    meta.update({'playcount': 0, 'overlay': 0})
                    poster = season_meta[i]['cover_url']
                    playcountMenu = language(30403).encode("utf-8")
                    if season_meta[i]['overlay'] == 6: playcountMenu = language(30404).encode("utf-8")
                    metaimdb, metaseason = urllib.quote_plus(re.sub('[^0-9]', '', str(season_meta[i]['imdb_id']))), urllib.quote_plus(str(season_meta[i]['season']))
                    if poster == '': poster = image
                    if banner == '': banner = poster
                    if banner == '': banner = image
                else:
                    poster, banner = image, image

                meta.update({'label': name, 'title': name, 'art(season.banner)': banner, 'art(season.poster': poster})

                cm = []
                cm.append((language(30415).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s)' % (sys.argv[0], sysshow)))
                if getSetting("meta") == 'true':
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=metadata_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

        xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(seasons)'):
                return index().container_view('seasons', {'skin.confluence' : 500})
            xbmc.sleep(100)

    def episodeList(self, episodeList):
        if episodeList == None: return

        autoplay = getSetting("autoplay")
        if PseudoTV == 'True': autoplay = 'true'

        getmeta = getSetting("meta")
        if action == 'episodes_added' and not (not (link().trakt_user == '' or link().trakt_password == '') and getSetting("trakt_episodes") == 'true'): getmeta = ''
        if action == 'episodes2' or action == 'episodes_calendar': getmeta = ''

        total = len(episodeList)
        for i in episodeList:
            try:
                name, title, year, imdb, tvdb, tvrage, url, image, genre, plot, date, show, show_alt, season, episode = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['tvrage'], i['url'], i['image'], i['genre'], i['plot'], i['date'], i['show'], i['show_alt'], i['season'], i['episode']
                if plot == '0': plot = addonDesc

                sysname, systitle, sysyear, sysimdb, systvdb, systvrage, sysurl, sysimage, sysgenre, sysplot, sysdate, sysshow, sysshow_alt, sysseason, sysepisode = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(tvrage), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(date), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(season), urllib.quote_plus(episode)

                if not autoplay == 'false':
                    u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, systvrage, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                    isFolder = False
                else:
                    u = '%s?action=get_host&name=%s&title=%s&year=%s&imdb=%s&url=%s&image=%s&genre=%s&plot=%s&tvdb=%s&tvrage=%s&date=%s&show=%s&show_alt=%s&season=%s&episode=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl, sysimage, sysgenre, sysplot, systvdb, systvrage, sysdate, sysshow, sysshow_alt, sysseason, sysepisode)
                    isFolder = True

                if getmeta == 'true':
                    imdb = re.sub('[^0-9]', '', imdb)
                    meta = metaget.get_episode_meta(title, imdb, season, episode)
                    meta.update({'tvshowtitle': show})
                    if meta['title'] == '': meta.update({'title': title})
                    if meta['episode'] == '': meta.update({'episode': episode})
                    if meta['premiered'] == '': meta.update({'premiered': date})
                    if meta['plot'] == '': meta.update({'plot': plot})
                    playcountMenu = language(30403).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30404).encode("utf-8")
                    metaimdb, metaseason, metaepisode = urllib.quote_plus(re.sub('[^0-9]', '', str(meta['imdb_id']))), urllib.quote_plus(str(meta['season'])), urllib.quote_plus(str(meta['episode']))
                    label = str(meta['season']) + 'x' + '%02d' % int(meta['episode']) + ' . ' + meta['title']
                    if action == 'episodes2' or action == 'episodes_added' or action == 'episodes_calendar': label = show + ' - ' + label
                    poster = meta['cover_url']
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'year' : year, 'premiered' : date, 'genre' : genre, 'plot': plot}
                    label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                    if action == 'episodes2' or action == 'episodes_added' or action == 'episodes_calendar': label = show + ' - ' + label
                    poster = image
                if getmeta == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=toggle_episode_playback&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s)' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, systvrage, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre)))
                cm.append((language(30416).encode("utf-8"), 'Action(Info)'))
                if getmeta == 'true':
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=metadata_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                    cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=isFolder)
            except:
                pass

        try:
            next = episodeList[0]['next']
            if next == '': raise Exception()
            name, url, image = language(30361).encode("utf-8"), next, os.path.join(addonArt,'item_next2.jpg')
            if getSetting("appearance") == '-': image = 'DefaultFolder.png'
            u = '%s?action=episodes2&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
            item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
            item.setProperty("Fanart_Image", addonFanart)
            item.addContextMenuItems([], replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
        except:
            pass

        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
        for i in range(0, 200):
            if xbmc.getCondVisibility('Container.Content(episodes)'):
                return index().container_view('episodes', {'skin.confluence' : 504})
            xbmc.sleep(100)

    def moviesourceList(self, sourceList):
        if sourceList == None: return

        try:
            name, title, year, imdb, image, genre, plot = sourceList[0]['name'], sourceList[0]['title'], sourceList[0]['year'], sourceList[0]['imdb'], sourceList[0]['image'], sourceList[0]['genre'], sourceList[0]['plot']
            if plot == '0': plot = addonDesc

            if getSetting("meta") == 'true':
                meta = metaget.get_meta('movie', title ,year=year)
                meta.update({'playcount': 0, 'overlay': 0})
                trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                if trailer == '': trailer = urllib.quote_plus(name)
                if poster == '': poster = image
            else:
                meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                trailer, poster = urllib.quote_plus(name), image
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                sysname, sysurl, sysimdb, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(imdb), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_moviehost&name=%s&url=%s&imdb=%s&source=%s&provider=%s&t=%s' % (sys.argv[0], sysname, sysurl, sysimdb, syssource, sysprovider, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

    def tvsourceList(self, sourceList):
        if sourceList == None: return

        try:
            name, title, year, imdb, tvdb, image, genre, plot, date, show, show_alt, season, episode = sourceList[0]['name'], sourceList[0]['title'], sourceList[0]['year'], sourceList[0]['imdb'], sourceList[0]['tvdb'], sourceList[0]['image'], sourceList[0]['genre'], sourceList[0]['plot'], sourceList[0]['date'], sourceList[0]['show'], sourceList[0]['show_alt'], sourceList[0]['season'], sourceList[0]['episode']
            if plot == '0': plot = addonDesc

            if getSetting("meta") == 'true':
                imdb = re.sub('[^0-9]', '', imdb)
                meta = metaget.get_episode_meta(title, imdb, season, episode)
                meta.update({'playcount': 0, 'overlay': 0})
                meta.update({'tvshowtitle': show})
                if meta['title'] == '': meta.update({'title': title})
                if meta['episode'] == '': meta.update({'episode': episode})
                if meta['premiered'] == '': meta.update({'premiered': date})
                if meta['plot'] == '': meta.update({'plot': plot})
                poster = meta['cover_url']
                if poster == '': poster = image
            else:
                meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'year' : year, 'premiered' : date, 'genre' : genre, 'plot': plot}
                poster = image
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(sourceList)
        for i in sourceList:
            try:
                url, source, provider = i['url'], i['source'], i['provider']
                sysname, sysurl, sysimdb, syssource, sysprovider = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(imdb), urllib.quote_plus(source), urllib.quote_plus(provider)

                u = '%s?action=play_tvhost&name=%s&url=%s&imdb=%s&source=%s&provider=%s&t=%s' % (sys.argv[0], sysname, sysurl, sysimdb, syssource, sysprovider, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s&provider=%s)' % (sys.argv[0], sysname, sysurl, sysprovider)))
                cm.append((language(30416).encode("utf-8"), 'Action(Info)'))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))

                item = xbmcgui.ListItem(source, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

        xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

class contextMenu:
    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def cache_clear(self):
        try: StorageServer.StorageServer(addonFullId,1).delete('%')
        except: pass
        try: StorageServer.StorageServer(addonFullId,24).delete('%')
        except: pass
        try: StorageServer.StorageServer(addonFullId,720).delete('%')
        except: pass
        index().infoDialog(language(30312).encode("utf-8"))

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self, id=addonId):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % id)

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"|"%s"|"' % (skin, content) in i]
            write.append('"%s"|"%s"|"%s"' % (skin, content, str(view)))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(viewData, 'w')
            file.write(str(write))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb, year, refresh=False):
        try:
            if refresh == True: index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if '"%s"' % url in read:
                index().infoDialog(language(30305).encode("utf-8"), name)
                return
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write.append('"%s"|"%s"|"%s"|"%s"|"%s"' % (name, year, imdb, url, image))
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            write = [i.strip('\n').strip('\r') for i in read.splitlines(True) if i.strip('\r\n')]
            write = [i for i in write if not '"%s"' % url in i]
            write = '\r\n'.join(write)
            file = xbmcvfs.File(data, 'w')
            file.write(str(write))
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def trakt_manager(self, content, name, imdb):
        try:
            if not imdb.startswith('tt'): imdb = 'tt' + imdb

            userList = userlists().trakt_list()

            nameList = [i['name'] for i in userList]
            nameList = [nameList[i//2] for i in range(len(nameList)*2)]
            for i in range(0, len(nameList), 2): nameList[i] = (language(30427) + ' ' + nameList[i]).encode('utf-8')
            for i in range(1, len(nameList), 2): nameList[i] = (language(30428) + ' ' + nameList[i]).encode('utf-8')
            nameList = [language(30422).encode("utf-8"), language(30423).encode("utf-8"), language(30424).encode("utf-8"), language(30425).encode("utf-8"), language(30426).encode("utf-8")] + nameList

            slugList = [[x for x in i['url'].split('/') if not x == ''][-1] for i in userList]
            slugList = [slugList[i//2] for i in range(len(slugList)*2)]
            slugList = ['', '', '', '', ''] + slugList

            select = index().selectDialog(nameList, language(30421).encode("utf-8"))
            post = {"imdb_id": imdb, "movies": [{"imdb_id": imdb}], "shows": [{"imdb_id": imdb}]}

            if select == -1:
                return
            elif select == 0:
                url = 'http://api.trakt.tv/%s/library/%s' % (content, link().trakt_key)
            elif select == 1:
                url = 'http://api.trakt.tv/%s/unlibrary/%s' % (content, link().trakt_key)
            elif select == 2:
                url = 'http://api.trakt.tv/%s/watchlist/%s' % (content, link().trakt_key)
            elif select == 3:
                url = 'http://api.trakt.tv/%s/unwatchlist/%s' % (content, link().trakt_key)
            else:
                if select == 4:
                    new = common.getUserInput(language(30426).encode("utf-8"), '')
                    if (new is None or new == ''): return
                    url = 'http://api.trakt.tv/lists/add/%s' % link().trakt_key
                    post = {"name": new, "privacy": "private", "description": ""}
                    post.update({"username": link().trakt_user, "password": link().trakt_password})
                    result = getUrl(url, post=json.dumps(post)).result
                    result = json.loads(result)
                    if result['status'] == 'failure':
                        return index().infoDialog(result['error'].encode("utf-8"), name)
                    slug = result['slug']
                else:
                    slug = slugList[select]

                if select == 4 or not select % 2 == 0:
                    url = 'http://api.trakt.tv/lists/items/add/%s' % link().trakt_key
                else:
                    url = 'http://api.trakt.tv/lists/items/delete/%s' % link().trakt_key

                post = {"slug": slug, "items": [{"type": "movie", "imdb_id": imdb}, {"type": "show", "imdb_id": imdb}]}


            post.update({"username": link().trakt_user, "password": link().trakt_password})
            result = getUrl(url, post=json.dumps(post)).result
            result = json.loads(result)

            try: info = result['status'].encode("utf-8")
            except: pass
            try: info = result['message'].encode("utf-8")
            except: pass
            try:
                if result['already_exist'] == 1: info = 'already added'
            except: pass
            try:
                if result['inserted'] == 1: info = 'added successfully'
            except: pass

            index().infoDialog(info, name)
        except:
            return

    def metadata(self, content, imdb, season, episode):
        try:
            if content == 'movie' or content == 'tvshow':
                metaget.update_meta(content, '', imdb, year='')
                index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library_movie_add(self, name, title, year, imdb, url):
        try:
            monadic = self.movie_library(name, title, year, imdb, url, check=True)
            if monadic == False:
                yes = index().yesnoDialog(language(30347).encode("utf-8"), language(30349).encode("utf-8"), name)
                if yes: self.movie_library(name, title, year, imdb, url)
                else: return

            index().infoDialog(language(30309).encode("utf-8"), name)
            if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('UpdateLibrary(video,%s)' % movieLibrary)
        except:
            return

    def library_movie_list(self, url):
        try:
            yes = index().yesnoDialog(language(30350).encode("utf-8"), language(30352).encode("utf-8"))
            if yes: duplicate = False
            else: duplicate = True

            match = movies().get(url, idx=False)
            if match == None: return

            #dialog = xbmcgui.DialogProgress()
            #dialog.create(addonName.encode("utf-8"), language(30409).encode("utf-8"))

            for i in range(len(match)):
                if xbmc.abortRequested == True: sys.exit()
                if xbmc.abortRequested == True: return

                #if dialog.iscanceled(): dialog.close()
                #if dialog.iscanceled(): return
                #dialog.update(int((100 / float(len(match))) * i), language(30409).encode("utf-8"), str(match[i]['name']))

                if duplicate == False: 
                    self.movie_library(match[i]['name'], match[i]['title'], match[i]['year'], match[i]['imdb'], match[i]['url'], check=True)
                else: 
                    self.movie_library(match[i]['name'], match[i]['title'], match[i]['year'], match[i]['imdb'], match[i]['url'])

            #dialog.close()

            index().infoDialog(language(30309).encode("utf-8"))
            if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('UpdateLibrary(video,%s)' % movieLibrary)
        except:
            return

    def library_tv_add(self, name, year, imdb, url):
        try:
            monadic = self.tv_library(name, year, imdb, url, check=True)
            if monadic == False:
                yes = index().yesnoDialog(language(30348).encode("utf-8"), language(30349).encode("utf-8"), name)
                if yes: self.tv_library(name, year, imdb, url)
                else: return

            index().infoDialog(language(30310).encode("utf-8"), name)
            if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('UpdateLibrary(video,%s)' % tvLibrary)
        except:
            return

    def library_tv_list(self, url):
        try:
            yes = index().yesnoDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"))
            if yes: duplicate = False
            else: duplicate = True

            match = shows().get(url, idx=False)
            if match == None: return

            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), language(30409).encode("utf-8"))

            for i in range(len(match)):
                if xbmc.abortRequested == True: sys.exit()
                if xbmc.abortRequested == True: return

                if dialog.iscanceled(): dialog.close()
                if dialog.iscanceled(): return
                dialog.update(int((100 / float(len(match))) * i), language(30409).encode("utf-8"), str(match[i]['name']))

                if duplicate == False: 
                    self.tv_library(match[i]['name'], match[i]['year'], match[i]['imdb'], match[i]['url'], check=True)
                else: 
                    self.tv_library(match[i]['name'], match[i]['year'], match[i]['imdb'], match[i]['url'])

            dialog.close()

            index().infoDialog(language(30310).encode("utf-8"))
            if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('UpdateLibrary(video,%s)' % tvLibrary)
        except:
            return

    def library_update(self, silent=False):
        try:
            match = []

            seasons, episodes = [], []
            shows = [os.path.join(tvLibrary, i) for i in xbmcvfs.listdir(tvLibrary)[0]]
            for show in shows: seasons += [os.path.join(show, i) for i in xbmcvfs.listdir(show)[0]]
            for season in seasons: episodes += [os.path.join(season, i) for i in xbmcvfs.listdir(season)[1] if i.endswith('.strm')]

            for episode in episodes:
                try:
                    file = xbmcvfs.File(episode)
                    read = file.read()
                    read = read.encode("utf-8")
                    file.close()
                    if not read.startswith(sys.argv[0]): raise Exception()
                    params = {}
                    query = read[read.find('?') + 1:].split('&')
                    for i in query: params[i.split('=')[0]] = i.split('=')[1]
                    show, show_alt, year, imdb, tvdb = urllib.unquote_plus(params["show"]), urllib.unquote_plus(params["show_alt"]), urllib.unquote_plus(params["year"]), urllib.unquote_plus(params["imdb"]), urllib.unquote_plus(params["tvdb"])
                    match.append({'show': show, 'show_alt': show_alt, 'year': year, 'imdb': imdb, 'tvdb': tvdb})
                except:
                    pass

            match = [i for x, i in enumerate(match) if i not in match[x + 1:]]
            if len(match) == 0: return

            if silent == False:
                dialog = xbmcgui.DialogProgress()
                dialog.create(addonName.encode("utf-8"), language(30410).encode("utf-8"))

            for i in range(len(match)):
                if xbmc.abortRequested == True: sys.exit()
                if xbmc.abortRequested == True: return

                if silent == False:
                    if dialog.iscanceled(): dialog.close()
                    if dialog.iscanceled(): return
                    dialog.update(int((100 / float(len(match))) * i), language(30410).encode("utf-8"), str(match[i]['show']))

                self.tv_library(match[i]['show'], match[i]['year'], match[i]['imdb'], '', match[i]['show_alt'], match[i]['tvdb'])

            if silent == False: dialog.close()
        except:
            pass

        if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'):
            xbmc.executebuiltin('UpdateLibrary(video)')
        if silent == False:
            index().infoDialog(language(30311).encode("utf-8"))

    def library_preset_list(self, url):
        if xbmc.getInfoLabel('Container.FolderPath').endswith('root_tools'):
            yes = index().yesnoDialog(language(30353).encode("utf-8"), '')
            if not yes: return

        if url == 'trakt_collection':
            self.library_movie_list(link().trakt_collection % (link().trakt_key, link().trakt_user))
        elif url == 'trakt_watchlist':
            self.library_movie_list(link().trakt_watchlist % (link().trakt_key, link().trakt_user))
        elif url == 'imdb_watchlist':
            self.library_movie_list(link().imdb_watchlist % link().imdb_user)
        elif url == 'trakt_tv_collection':
            self.library_tv_list(link().trakt_tv_collection % (link().trakt_key, link().trakt_user))
        elif url == 'trakt_tv_watchlist':
            self.library_tv_list(link().trakt_tv_watchlist % (link().trakt_key, link().trakt_user))
        elif url == 'imdb_tv_watchlist':
            self.library_tv_list(link().imdb_watchlist % link().imdb_user)

    def movie_library(self, name, title, year, imdb, url, check=False):
        try:
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(movieLibrary)
            sysname, systitle, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(url)
            content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, sysurl)
            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            folder = os.path.join(movieLibrary, enc_name)
            stream = os.path.join(folder, enc_name + '.strm')
        except:
            return

        try:
            if check == False: raise Exception()
            data = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber", "file"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            data = unicode(data, 'utf-8', errors='ignore')
            data = json.loads(data)
            data = data['result']['movies']
            data = [i for i in data if imdb in i['imdbnumber']][0]
            if data['file'] == stream: raise Exception()
            return False
        except:
            pass

        try:
            xbmcvfs.mkdir(folder)
            file = xbmcvfs.File(stream, 'w')
            file.write(str(content))
            file.close()
        except:
            return

    def tv_library(self, name, year, imdb, url, show_alt='', tvdb='', check=False):
        try:
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(tvLibrary)
            show = name

            seasonList = seasons().get(url, year, imdb, '', '', '', show, show_alt, tvdb, idx=False)
            year, tvdb = seasonList[0]['year'], seasonList[0]['tvdb']
            if tvdb == '0': return
        except:
            return

        try:
            if check == False: raise Exception()
            data = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
            data = unicode(data, 'utf-8', errors='ignore')
            data = json.loads(data)
            data = data['result']['tvshows']
            data = [i for i in data if tvdb in i['imdbnumber']][0]
            return False
        except:
            pass

        try:
            for i in seasonList:
                season, seasonUrl, tvdb, genre, show_alt, idx_data = i['name'], i['url'], i['tvdb'], i['genre'], i['show_alt'], i['idx_data']
                enc_show = show_alt.translate(None, '\/:*?"<>|').strip('.')
                folder = os.path.join(tvLibrary, enc_show)
                xbmcvfs.mkdir(folder)
                enc_season = season.translate(None, '\/:*?"<>|').strip('.')
                seasonDir = os.path.join(folder, enc_season)
                xbmcvfs.mkdir(seasonDir)
                episodeList = episodes().get(season, seasonUrl, year, imdb, tvdb, '', genre, '', show, show_alt, idx_data, idx=False)

                for i in episodeList:
                    name, title, year, imdb, tvdb, season, episode, show, show_alt, date, genre, url = i['name'], i['title'], i['year'], i['imdb'], i['tvdb'], i['season'], i['episode'], i['show'], i['show_alt'], i['date'], i['genre'], i['url']
                    sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre), urllib.quote_plus(url)
                    content = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s&url=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre, sysurl)

                    enc_name = name.translate(None, '\/:*?"<>|').strip('.')
                    stream = os.path.join(seasonDir, enc_name + '.strm')
                    file = xbmcvfs.File(stream, 'w')
                    file.write(str(content))
                    file.close()
        except:
            return

    def download(self, name, url, provider):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|').strip('.')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file is None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().sources_resolve(url, provider)
            if url is None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '' or ext == 'php': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30306).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30307).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30308).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def toggle_playback(self, content, name, title, year, imdb, tvdb, tvrage, season, episode, show, show_alt, date, genre):
        if content == 'movie':
            meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'), 'year': xbmc.getInfoLabel('ListItem.year'), 'genre': xbmc.getInfoLabel('ListItem.genre'), 'director': xbmc.getInfoLabel('ListItem.director'), 'country': xbmc.getInfoLabel('ListItem.country'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'votes': xbmc.getInfoLabel('ListItem.votes'), 'mpaa': xbmc.getInfoLabel('ListItem.mpaa'), 'duration': xbmc.getInfoLabel('ListItem.duration'), 'trailer': xbmc.getInfoLabel('ListItem.trailer'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'studio': xbmc.getInfoLabel('ListItem.studio'), 'tagline': xbmc.getInfoLabel('ListItem.tagline'), 'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
            label, poster, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
            sysname, systitle, sysyear, sysimdb = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb)
            u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb)

        elif content == 'episode':
            meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle'), 'season': xbmc.getInfoLabel('ListItem.season'), 'episode': xbmc.getInfoLabel('ListItem.episode'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'director': xbmc.getInfoLabel('ListItem.director'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'duration': xbmc.getInfoLabel('ListItem.duration'), 'premiered': xbmc.getInfoLabel('ListItem.premiered'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
            label, poster, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
            sysname, systitle, sysyear, sysimdb, systvdb, systvrage, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(tvrage), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date), urllib.quote_plus(genre)
            u = '%s?action=play&name=%s&title=%s&year=%s&imdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s&genre=%s' % (sys.argv[0], sysname, systitle, sysyear, sysimdb, systvdb, systvrage, sysseason, sysepisode, sysshow, sysshow_alt, sysdate, sysgenre)

        autoplay = getSetting("autoplay")
        if not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
            autoplay = getSetting("autoplay_library")
        if autoplay == 'false': u += '&url=direct://'
        else: u += '&url=dialog://'

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
        item.setInfo( type="Video", infoLabels= meta )
        item.setProperty("IsPlayable", "true")
        item.setProperty("Video", "true")
        item.setProperty("Fanart_Image", fanart)
        xbmc.Player().play(u, item)

    def trailer(self, name, url):
        url = trailer().run(name, url)
        if url is None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        xbmc.Player().play(url, item)

class favourites:
    def __init__(self):
        self.list = []

    def movies(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for title, year, imdb, url, image in match:
            name = '%s (%s)' % (title, year)
            self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': '0', 'plot': '0'})
        self.list = sorted(self.list, key=itemgetter('name'))
        index().movieList(self.list)

    def shows(self):
        file = xbmcvfs.File(favData2)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '0', 'plot': '0'})
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'root_movies.jpg', 'action': 'root_movies'})
        rootList.append({'name': 30502, 'image': 'root_shows.jpg', 'action': 'root_shows'})
        rootList.append({'name': 30503, 'image': 'channels_movies.jpg', 'action': 'channels_movies'})
        rootList.append({'name': 30504, 'image': 'root_genesis.jpg', 'action': 'root_genesis'})
        rootList.append({'name': 30505, 'image': 'movies_added.jpg', 'action': 'movies_added'})
        rootList.append({'name': 30506, 'image': 'episodes_added.jpg', 'action': 'episodes_added'})
        rootList.append({'name': 30507, 'image': 'calendar_episodes.jpg', 'action': 'calendar_episodes'})
        rootList.append({'name': 30508, 'image': 'root_tools.jpg', 'action': 'root_tools'})
        rootList.append({'name': 30509, 'image': 'root_search.jpg', 'action': 'root_search'})
        index().rootList(rootList)

    def movies(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'genres_movies.jpg', 'action': 'genres_movies'})
        rootList.append({'name': 30522, 'image': 'movies_boxoffice.jpg', 'action': 'movies_boxoffice'})
        rootList.append({'name': 30523, 'image': 'years_movies.jpg', 'action': 'years_movies'})
        rootList.append({'name': 30524, 'image': 'movies_trending.jpg', 'action': 'movies_trending'})
        rootList.append({'name': 30525, 'image': 'movies_popular.jpg', 'action': 'movies_popular'})
        rootList.append({'name': 30526, 'image': 'movies_views.jpg', 'action': 'movies_views'})
        rootList.append({'name': 30527, 'image': 'movies_oscars.jpg', 'action': 'movies_oscars'})
        rootList.append({'name': 30528, 'image': 'actors_movies.jpg', 'action': 'actors_movies'})
        rootList.append({'name': 30529, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'genres_shows.jpg', 'action': 'genres_shows'})
        rootList.append({'name': 30542, 'image': 'shows_popular.jpg', 'action': 'shows_popular'})
        rootList.append({'name': 30543, 'image': 'shows_active.jpg', 'action': 'shows_active'})
        rootList.append({'name': 30544, 'image': 'shows_trending.jpg', 'action': 'shows_trending'})
        rootList.append({'name': 30545, 'image': 'shows_rating.jpg', 'action': 'shows_rating'})
        rootList.append({'name': 30546, 'image': 'shows_views.jpg', 'action': 'shows_views'})
        rootList.append({'name': 30547, 'image': 'actors_shows.jpg', 'action': 'actors_shows'})
        rootList.append({'name': 30548, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        index().rootList(rootList)

    def genesis(self):
        rootList = []
        if not (link().trakt_user == '' or link().trakt_password == ''):
            rootList.append({'name': 30561, 'image': 'movies_trakt_collection.jpg', 'action': 'movies_trakt_collection'})
            rootList.append({'name': 30562, 'image': 'shows_trakt_collection.jpg', 'action': 'shows_trakt_collection'})
            rootList.append({'name': 30563, 'image': 'movies_trakt_watchlist.jpg', 'action': 'movies_trakt_watchlist'})
            rootList.append({'name': 30564, 'image': 'shows_trakt_watchlist.jpg', 'action': 'shows_trakt_watchlist'})
        if not (link().imdb_user == ''):
            rootList.append({'name': 30565, 'image': 'movies_imdb_watchlist.jpg', 'action': 'movies_imdb_watchlist'})
            rootList.append({'name': 30566, 'image': 'shows_imdb_watchlist.jpg', 'action': 'shows_imdb_watchlist'})
        if not (link().trakt_user == '' or link().trakt_password == '') or not (link().imdb_user == ''):
            rootList.append({'name': 30567, 'image': 'userlists_movies.jpg', 'action': 'userlists_movies'})
            rootList.append({'name': 30568, 'image': 'userlists_shows.jpg', 'action': 'userlists_shows'})
        rootList.append({'name': 30569, 'image': 'movies_favourites.jpg', 'action': 'movies_favourites'})
        rootList.append({'name': 30570, 'image': 'shows_favourites.jpg', 'action': 'shows_favourites'})
        rootList.append({'name': 30571, 'image': 'folder_downloads.jpg', 'action': 'folder_downloads'})
        index().rootList(rootList)

    def search(self):
        rootList = []
        rootList.append({'name': 30581, 'image': 'movies_search.jpg', 'action': 'movies_search'})
        rootList.append({'name': 30582, 'image': 'shows_search.jpg', 'action': 'shows_search'})
        rootList.append({'name': 30583, 'image': 'actors_movies.jpg', 'action': 'actors_movies'})
        rootList.append({'name': 30584, 'image': 'actors_shows.jpg', 'action': 'actors_shows'})
        index().rootList(rootList)

    def tools(self):
        rootList = []
        rootList.append({'name': 30601, 'image': 'settings_open.jpg', 'action': 'settings_open'})
        rootList.append({'name': 30602, 'image': 'settings_metahandler.jpg', 'action': 'settings_metahandler'})
        rootList.append({'name': 30603, 'image': 'settings_urlresolver.jpg', 'action': 'settings_urlresolver'})
        rootList.append({'name': 30604, 'image': 'cache_clear.jpg', 'action': 'cache_clear'})
        rootList.append({'name': 30605, 'image': 'library_update.jpg', 'action': 'library_update'})
        if not (link().trakt_user == '' or link().trakt_password == ''):
            rootList.append({'name': 30606, 'image': 'movies_trakt_collection.jpg', 'action': 'library_trakt_collection'})
            rootList.append({'name': 30607, 'image': 'shows_trakt_collection.jpg', 'action': 'library_tv_trakt_collection'})
            rootList.append({'name': 30608, 'image': 'movies_trakt_watchlist.jpg', 'action': 'library_trakt_watchlist'})
            rootList.append({'name': 30609, 'image': 'shows_trakt_watchlist.jpg', 'action': 'library_tv_trakt_watchlist'})
        if not (link().imdb_user == ''):
            rootList.append({'name': 30610, 'image': 'movies_imdb_watchlist.jpg', 'action': 'library_imdb_watchlist'})
            rootList.append({'name': 30611, 'image': 'shows_imdb_watchlist.jpg', 'action': 'library_tv_imdb_watchlist'})
        rootList.append({'name': 30612, 'image': 'folder_movie.jpg', 'action': 'folder_movie'})
        rootList.append({'name': 30613, 'image': 'folder_tv.jpg', 'action': 'folder_tv'})
        index().rootList(rootList)


class link:
    def __init__(self):
        self.imdb_base = 'http://www.imdb.com'
        self.imdb_akas = 'http://akas.imdb.com'
        self.imdb_mobile = 'http://m.imdb.com'
        self.imdb_genre = 'http://akas.imdb.com/genre/'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_seasons = 'http://akas.imdb.com/title/tt%s/episodes'
        self.imdb_episodes = 'http://www.imdb.com/title/tt%s/episodes?season=%s'
        self.imdb_image = 'http://i.media-imdb.com/images/SFaa265aa19162c9e4f3781fbae59f856d/nopicture/medium/film.png'
        self.imdb_tv_image = 'http://i.media-imdb.com/images/SF1b61b592d2fa1b9cfb8336f160e1efcf/nopicture/medium/tv.png'
        self.imdb_genres = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&genres=%s'
        self.imdb_years = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=25&start=1&&year=%s,%s'
        self.imdb_popular = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1'
        self.imdb_boxoffice = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us,desc&count=25&start=1'
        self.imdb_views = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=num_votes,desc&count=25&start=1'
        self.imdb_oscars = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&groups=oscar_best_picture_winners&sort=year,desc&count=25&start=1'
        self.imdb_search = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=moviemeter,asc&count=25&start=1&title=%s'
        self.imdb_tv_genres = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&genres=%s'
        self.imdb_tv_popular = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1'
        self.imdb_tv_rating = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&sort=user_rating,desc&count=25&start=1'
        self.imdb_tv_views = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=num_votes,desc&count=25&start=1'
        self.imdb_tv_active = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&production_status=active&sort=moviemeter,asc&count=25&start=1'
        self.imdb_tv_search = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&title=%s'
        self.imdb_api_search = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'
        self.imdb_actors_search = 'http://www.imdb.com/search/name?count=100&name=%s'
        self.imdb_actors = 'http://m.imdb.com/name/nm%s/filmotype/%s'
        self.imdb_userlists = 'http://akas.imdb.com/user/ur%s/lists?tab=all&sort=modified:desc&filter=titles'
        self.imdb_watchlist ='http://akas.imdb.com/user/ur%s/watchlist?sort=alpha,asc&mode=detail&page=1'
        self.imdb_list ='http://akas.imdb.com/list/%s/?view=detail&count=100&sort=listorian:asc&start=1'
        self.imdb_user = getSetting("imdb_user").replace('ur', '')

        self.tvdb_base = 'http://thetvdb.com'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.tvdb_search = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=tt%s&language=en'
        self.tvdb_search2 = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=en'
        self.tvdb_episodes = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'
        self.tvdb_poster = 'http://thetvdb.com/banners/'
        self.tvdb_thumb = 'http://thetvdb.com/banners/_cache/'

        self.trakt_base = 'http://api.trakt.tv'
        self.trakt_key = base64.urlsafe_b64decode('YmU2NDI5MWFhZmJiYmU2MmZkYzRmM2FhMGVkYjQwNzM=')
        self.trakt_user, self.trakt_password = getSetting("trakt_user"), getSetting("trakt_password")
        self.trakt_trending = 'http://api.trakt.tv/movies/trending.json/%s'
        self.trakt_watchlist = 'http://api.trakt.tv/user/watchlist/movies.json/%s/%s'
        self.trakt_collection = 'http://api.trakt.tv/user/library/movies/collection.json/%s/%s'
        self.trakt_tv_search = 'http://api.trakt.tv/show/summary.json/%s/%s'
        self.trakt_tv_trending = 'http://api.trakt.tv/shows/trending.json/%s'
        self.trakt_tv_calendar = 'http://api.trakt.tv/calendar/shows.json/%s/%s/%s'
        self.trakt_tv_user_calendar = 'http://api.trakt.tv/user/calendar/shows.json/%s/%s/%s/%s'
        self.trakt_tv_watchlist = 'http://api.trakt.tv/user/watchlist/shows.json/%s/%s'
        self.trakt_tv_collection = 'http://api.trakt.tv/user/library/shows/collection.json/%s/%s'
        self.trakt_lists = 'http://api.trakt.tv/user/lists.json/%s/%s'
        self.trakt_list= 'http://api.trakt.tv/user/list.json/%s/%s'

        self.tvrage_base = 'http://services.tvrage.com'
        self.tvrage_search = 'http://services.tvrage.com/feeds/showinfo.php?sid=%s'
        self.tvrage_search2 = 'http://services.tvrage.com/feeds/search.php?show=%s'
        self.tvrage_info = 'http://www.tvrage.com/shows/id-%s/episode_list/all'
        self.epguides_info = 'http://epguides.com/common/exportToCSV.asp?rage=%s'

        self.scn_base = 'http://www.scnsrc.me'
        self.scn_added = 'http://www.scnsrc.me/category/films/bluray/page/1/'
        self.scn_tv_added = 'http://www.scnsrc.me/category/tv/page/1/'

class actors:
    def __init__(self):
        self.list = []

    def movies(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_actors_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            for i in range(0, len(self.list)): self.list[i].update({'action': 'movies'})
            index().rootList(self.list)

    def shows(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_actors_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            for i in range(0, len(self.list)): self.list[i].update({'action': 'shows'})
            index().rootList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            actors = common.parseDOM(result, "tr", attrs = { "class": ".+? detailed" })
        except:
            return
        for actor in actors:
            try:
                name = common.parseDOM(actor, "a", ret="title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(actor, "a", ret="href")[0]
                url = re.findall('nm(\d*)', url, re.I)[0]
                type = common.parseDOM(actor, "span", attrs = { "class": "description" })[0]
                if 'Actress' in type: type = 'actress'
                elif 'Actor' in type: type = 'actor'
                else: raise Exception()
                url = link().imdb_actors % (url, type)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(actor, "img", ret="src")[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def movies(self):
        #self.list = self.imdb_list()
        try: self.list = cache3(self.imdb_list)
        except: return
        for i in range(0, len(self.list)): self.list[i].update({'image': 'genres_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)

    def shows(self):
        #self.list = self.imdb_list2()
        try: self.list = cache3(self.imdb_list2)
        except: return
        for i in range(0, len(self.list)): self.list[i].update({'image': 'genres_shows.jpg', 'action': 'shows'})
        index().rootList(self.list)

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_genre).result
            result = common.parseDOM(result, "table", attrs = { "class": "genre-table" })[0]
            genres = common.parseDOM(result, "h3")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = name.split('<', 1)[0].rsplit('>', 1)[0].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                url = re.compile('/genre/(.+?)/').findall(url)[0]
                if url == 'documentary': raise Exception()
                url = link().imdb_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def imdb_list2(self):
        try:
            result = getUrl(link().imdb_genre).result
            result = common.parseDOM(result, "div", attrs = { "class": "article" })
            result = [i for i in result if str('"tv_genres"') in i][0]
            genres = common.parseDOM(result, "td")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                try: url = re.compile('genres=(.+?)&').findall(url)[0]
                except: url = re.compile('/genre/(.+?)/').findall(url)[0]
                url = link().imdb_tv_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class years:
    def __init__(self):
        self.list = []

    def movies(self):
        self.list = self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'years_movies.jpg', 'action': 'movies'})
        index().rootList(self.list)

    def imdb_list(self):
        year = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")

        for i in range(int(year)-0, int(year)-50, -1):
            name = str(i).encode('utf-8')
            url = link().imdb_years % (str(i), str(i))
            url = url.encode('utf-8')
            self.list.append({'name': name, 'url': url})

        return self.list

class calendar:
    def __init__(self):
        self.list = []

    def episodes(self):
        self.list = self.trakt_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'calendar_episodes.jpg', 'action': 'episodes_calendar'})
        index().rootList(self.list)

    def trakt_list(self):
        now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
        today = datetime.date(now.year, now.month, now.day)

        for i in range(0, 14):
            date = today - datetime.timedelta(days=i)
            date = str(date)
            date = date.encode('utf-8')
            self.list.append({'name': date, 'url': date})

        return self.list

class userlists:
    def __init__(self):
        self.list = []

    def movies(self):
        if not (link().trakt_user == '' or link().trakt_password == ''): self.trakt_list()
        if not (link().imdb_user == ''): self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists_movies.jpg', 'action': 'movies_userlist'})
        index().rootList(self.list)

    def shows(self):
        if not (link().trakt_user == '' or link().trakt_password == ''): self.trakt_list()
        if not (link().imdb_user == ''): self.imdb_list()
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists_movies.jpg', 'action': 'shows_userlist'})
        index().rootList(self.list)

    def trakt_list(self):
        post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})
        info = (link().trakt_key, link().trakt_user)

        try:
            userlists = []
            result = getUrl(link().trakt_lists % info, post=post).result
            userlists = json.loads(result)
        except:
            pass

        for userlist in userlists:
            try:
                name = userlist['name']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = userlist['slug']
                url = '%s/%s' % (link().trakt_list % info, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

    def imdb_list(self):
        try:
            userlists = []
            result = getUrl(link().imdb_userlists % link().imdb_user).result
            result = result.decode('iso-8859-1').encode('utf-8')
            userlists = common.parseDOM(result, "div", attrs = { "class": "list_name" })
        except:
            pass

        for userlist in userlists:
            try:
                name = common.parseDOM(userlist, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(userlist, "a", ret="href")[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url})
            except:
                pass

        return self.list

class channels:
    def __init__(self):
        self.list = []
        self.sky_now_link = 'http://epgservices.sky.com/5.1.1/api/2.0/channel/json/%s/now/nn/0'
        self.sky_programme_link = 'http://tv.sky.com/programme/channel/%s/%s/%s.json'

    def movies(self):
        threads = []

        threads.append(Thread(self.sky_list, '01', 'Sky Premiere', '1409'))
        threads.append(Thread(self.sky_list, '02', 'Sky Premiere +1', '1823'))
        threads.append(Thread(self.sky_list, '03', 'Sky Showcase', '1814'))
        threads.append(Thread(self.sky_list, '04', 'Sky Greats', '1815'))
        threads.append(Thread(self.sky_list, '05', 'Sky Disney', '1838'))
        threads.append(Thread(self.sky_list, '06', 'Sky Family', '1808'))
        threads.append(Thread(self.sky_list, '07', 'Sky Action', '1001'))
        threads.append(Thread(self.sky_list, '08', 'Sky Comedy', '1002'))
        threads.append(Thread(self.sky_list, '09', 'Sky Crime', '1818'))
        threads.append(Thread(self.sky_list, '10', 'Sky Sci Fi', '1807'))
        threads.append(Thread(self.sky_list, '11', 'Sky Select', '1811'))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.list = sorted(self.list, key=itemgetter('num'))
        index().channelList(self.list)

    def sky_list(self, num, channel, id):
        try:
            url = self.sky_now_link % id
            result = getUrl(url).result
            result = json.loads(result)
            match = result['listings'][id][0]['url']

            dt = self.uk_datetime()
            dt1 = '%04d' % dt.year + '-' + '%02d' % dt.month + '-' + '%02d' % dt.day
            dt2 = int(dt.hour)
            if (dt2 < 6): dt2 = 0
            elif (dt2 >= 6 and dt2 < 12): dt2 = 1
            elif (dt2 >= 12 and dt2 < 18): dt2 = 2
            elif (dt2 >= 18): dt2 = 3
            url = self.sky_programme_link % (id, str(dt1), str(dt2))

            result = getUrl(url).result
            result = json.loads(result)
            result = result['listings'][id]
            result = [i for i in result if i['url'] == match][0]

            y = result['d']
            y = re.findall('.+?[(](\d{4})[)]', y)[0].strip()

            t = result['t']
            t = t.replace('(%s)' % y, '').strip()

            imdb_api = self.imdb_api(t, y)
            if imdb_api == None: imdb_api = self.imdb_api(t, str(int(y)+1))
            if imdb_api == None: imdb_api = self.imdb_api(t, str(int(y)-1))
            if imdb_api == None: raise Exception()

            title, year, imdb, plot = imdb_api

            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            year = year.encode('utf-8')

            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')

            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            self.list.append({'name': channel, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': '0', 'image': '0', 'date': '0', 'genre': '0', 'plot': plot, 'num': num})
        except:
            return

    def imdb_api(self, t, y=''):
        try:
            search = 'http://www.imdbapi.com/?t=%s' % urllib.quote_plus(t)
            if not y == '': search += '&y=%s' % y
            search = getUrl(search).result
            search = json.loads(search)

            title, year, imdb, plot = search['Title'], search['Year'], search['imdbID'], search['Plot']
            return (title, year, imdb, plot)
        except:
            return

    def uk_datetime(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 0)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

class movies:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, url, idx=True):
        if url == link().imdb_watchlist % link().imdb_user:
            self.list = self.imdb_list4(url)
        elif url.startswith(link().imdb_base) or url.startswith(link().imdb_akas):
            #self.list = self.imdb_list(url)
            try: self.list = cache(self.imdb_list, url)
            except: return
        elif url.startswith(link().imdb_mobile):
            #self.list = self.imdb_list2(url)
            try: self.list = cache(self.imdb_list2, url)
            except: return
        elif url.startswith(link().trakt_base):
            self.list = self.trakt_list(url)
        elif url.startswith(link().scn_base):
            #self.list = self.scn_list(url)
            try: self.list = cache(self.scn_list, url)
            except: return
        else:
            self.list = self.imdb_list3(link().imdb_list % url)
            try: self.list = sorted(self.list, key=itemgetter('name'))
            except: return

        if idx == False: return self.list
        index().movieList(self.list)

    def popular(self):
        #self.list = self.imdb_list(link().imdb_popular)
        try: self.list = cache(self.imdb_list, link().imdb_popular)
        except: return
        index().movieList(self.list)

    def boxoffice(self):
        #self.list = self.imdb_list(link().imdb_boxoffice)
        try: self.list = cache(self.imdb_list, link().imdb_boxoffice)
        except: return
        index().movieList(self.list)

    def views(self):
        #self.list = self.imdb_list(link().imdb_views)
        try: self.list = cache(self.imdb_list, link().imdb_views)
        except: return
        index().movieList(self.list)

    def oscars(self):
        #self.list = self.imdb_list(link().imdb_oscars)
        try: self.list = cache(self.imdb_list, link().imdb_oscars)
        except: return
        index().movieList(self.list)

    def added(self):
        #self.list = self.scn_list(link().scn_added)
        try: self.list = cache(self.scn_list, link().scn_added)
        except: return
        index().movieList(self.list)

    def trending(self):
        #self.list = self.trakt_list(link().trakt_trending % link().trakt_key)
        try: self.list = cache2(self.trakt_list, link().trakt_trending % link().trakt_key)
        except: return
        index().movieList(self.list[:100])

    def trakt_collection(self):
        self.list = self.trakt_list(link().trakt_collection % (link().trakt_key, link().trakt_user))
        index().movieList(self.list)

    def trakt_watchlist(self):
        self.list = self.trakt_list(link().trakt_watchlist % (link().trakt_key, link().trakt_user))
        index().movieList(self.list)

    def imdb_watchlist(self):
        self.list = self.imdb_list4(link().imdb_watchlist % link().imdb_user)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().movieList(self.list)

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().movieList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url.replace(link().imdb_base, link().imdb_akas)).result
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a")[1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = re.sub('[^0-9]', '', year)[:4]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    genre = common.parseDOM(movie, "span", attrs = { "class": "genre" })
                    genre = common.parseDOM(genre, "a")
                    genre = " / ".join(genre)
                    if genre == '': raise Exception()
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = '0'

                try:
                    plot = common.parseDOM(movie, "span", attrs = { "class": "outline" })[0]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'tvrage': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

    def imdb_list2(self, url):
        try:
            result = getUrl(url, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            movies = common.parseDOM(result, "div", attrs = { "class": "col-xs.+?" })
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "span", attrs = { "class": "h3" })[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "div", attrs = { "class": "unbold" })[0]
                year = re.sub("\n|[(]|[)]|\s", "", year)
                year = year.encode('utf-8')

                if not year.isdigit(): raise Exception()
                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = re.findall('tt(\d*)', url, re.I)[0]
                url = link().imdb_title % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'tvrage': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': '0', 'plot': '0'})
            except:
                pass

        return self.list

    def imdb_list3(self, url):
        try:
            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "pagination" })[0]
                pages = re.compile('.+?\d+.+?(\d+)').findall(pages)[0]

                for i in range(1, int(pages)):
                    self.data.append('')
                    moviesUrl = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    threads.append(Thread(self.thread, moviesUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            movies = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", attrs = { "onclick": ".+?" })[-1]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "year_type" })[0]
                year = year.replace('(', '').replace(')', '')
                year = year.encode('utf-8')

                if not year.isdigit(): raise Exception()
                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    plot = common.parseDOM(movie, "div", attrs = { "class": "item_description" })[0]
                    plot = plot.rsplit('<span>', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'tvrage': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': '0', 'plot': plot})
            except:
                pass

        return self.list

    def imdb_list4(self, url):
        try:
            URL = url.replace(link().imdb_base, link().imdb_akas)
            url = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(url))
            result = getUrl(url, referer=url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })
                pages = [re.compile('of (\d+) titles').findall(i)[0] for i in pages][0]
                pages = (int(pages)+100)/100
                for i in range(1, int(pages)):
                    self.data.append('')
                    moviesUrl = URL.replace('&page=1', '&page=%s' % str(i+1))
                    moviesUrl = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(moviesUrl))
                    threads.append(Thread(self.thread, moviesUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            movies = common.parseDOM(result, "div", attrs = { "class": "lister-item mode-detail" })
        except:
            return

        for movie in movies:
            try:
                title = common.parseDOM(movie, "h3", attrs = { "class": "lister-item-header" })[0]
                title = common.parseDOM(title, "a")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "span", attrs = { "class": "lister-item-year.+?" })[0]
                year = re.compile('[(](\d{4})[)]').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = common.parseDOM(movie, "img", ret="data-tconst")[0]
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(movie, "img", ret="src")[0]
                    image = urllib.unquote_plus(image)
                    image = image[image.find('?') + 1:].split('&')
                    image = [i.split('=', 1)[-1] for i in image if i.startswith('u=')][0]
                    image = 'http' + image.split('http' , 1)[-1]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    plot = common.parseDOM(movie, "p", attrs = { "class": "" })[0]
                    plot = plot.rsplit('<span>', 1)[0].rsplit('<a href', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'tvrage': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': '0', 'plot': plot})
            except:
                pass

        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post).result
            result = json.loads(result)

            movies = []
            try: result = result['items']
            except: pass
            for i in result:
                try: movies.append(i['movie'])
                except: pass
            if movies == []: 
                movies = result
        except:
            return

        for movie in movies:
            try:
                title = movie['title']
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = movie['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = movie['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: image = movie['images']['poster']
                except: image = movie['poster']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = movie['genres']
                    genre = " / ".join(genre)
                    if genre == '': raise Exception()
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = '0'

                try:
                    plot = movie['overview']
                    if plot == '': raise Exception()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'tvrage': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot})
            except:
                pass

        return self.list

    def scn_list(self, url):
        try:
            param = re.compile('(.+?/page/)(\d+)').findall(url)[0]

            threads = []
            for i in range(0, 3):
                self.data.append('')
                moviesUrl = param[0] + str(i+int(param[1])) + '/'
                threads.append(Thread(self.thread, moviesUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ''
            for i in self.data: result += i

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')

            movies = common.parseDOM(result, "div", attrs = { "class": "post" })
        except:
            return

        try:
            next = common.parseDOM(self.data[-1], "link", ret="href", attrs = { "rel": "next" })[0]
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "a", attrs = { "rel": "bookmark" })[0]
                title = re.compile('(.*) \d{4} ').findall(title)[0]
                title = title.replace("&#8216;", "'").replace("&#8217;", "'").replace("&#8211;", '-').replace("&#8230;", '.')
                title = common.replaceHTMLCodes(title)
                title = unicode(title.encode('utf-8'), 'ascii', 'ignore')
                title = title.encode('utf-8')

                year = common.parseDOM(movie, "a", attrs = { "rel": "bookmark" })[0]
                year = re.compile('.* (\d{4}) ').findall(year)[0]
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = re.compile('imdb.com/.+?tt(\d+)').findall(movie)[0]
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = link().imdb_image
                try: image = common.parseDOM(movie, "img", ret="src")[0]
                except: pass
                try: image = common.parseDOM(movie, "img", ret="src", attrs = { "height": "240" })[0]
                except: pass
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = re.compile('>Genre:<.+?>(.+?)<').findall(movie)[0]
                    genre = [i.strip() for i in genre.split(',')]
                    genre = " / ".join(genre)
                    if genre == '': raise Exception()
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = '0'

                try:
                    plot = movie.split('>Synopsis:<')[-1]
                    plot = common.parseDOM(plot, "span")[0]
                    if plot == '': raise Exception()
                    plot = plot.replace("&#8216;", "'").replace("&#8217;", "'").replace("&#8211;", '-').replace("&#8230;", '.')
                    plot = common.replaceHTMLCodes(plot)
                    plot = unicode(plot.encode('utf-8'), 'ascii', 'ignore')
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': '0', 'tvrage': '0', 'season': '0', 'episode': '0', 'show': '0', 'show_alt': '0', 'url': url, 'image': image, 'date': '0', 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        filter = []
        f = uniqueList([i['imdb'] for i in self.list]).list
        for x in f: filter += [[i for i in self.list if i['imdb'] == x][0]]
        self.list = filter

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url, referer=url).result
            self.data[i] = result
        except:
            return

class shows:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, url, idx=True):
        if url == link().imdb_watchlist % link().imdb_user:
            self.list = self.imdb_list4(url)
        elif url.startswith(link().imdb_base) or url.startswith(link().imdb_akas):
            #self.list = self.imdb_list(url)
            try: self.list = cache(self.imdb_list, url)
            except: return
        elif url.startswith(link().imdb_mobile):
            #self.list = self.imdb_list2(url)
            try: self.list = cache(self.imdb_list2, url)
            except: return
        elif url.startswith(link().trakt_base):
            self.list = self.trakt_list(url)
        else:
            self.list = self.imdb_list3(link().imdb_list % url)
            try: self.list = sorted(self.list, key=itemgetter('name'))
            except: return

        if idx == False: return self.list
        index().showList(self.list)

    def popular(self):
        #self.list = self.imdb_list(link().imdb_tv_popular)
        try: self.list = cache(self.imdb_list, link().imdb_tv_popular)
        except: return
        index().showList(self.list)

    def rating(self):
        #self.list = self.imdb_list(link().imdb_tv_rating)
        try: self.list = cache(self.imdb_list, link().imdb_tv_rating)
        except: return
        index().showList(self.list)

    def views(self):
        #self.list = self.imdb_list(link().imdb_tv_views)
        try: self.list = cache(self.imdb_list, link().imdb_tv_views)
        except: return
        index().showList(self.list)

    def active(self):
        #self.list = self.imdb_list(link().imdb_tv_active)
        try: self.list = cache(self.imdb_list, link().imdb_tv_active)
        except: return
        index().showList(self.list)

    def trending(self):
        #self.list = self.trakt_list(link().trakt_tv_trending % link().trakt_key)
        try: self.list = cache2(self.trakt_list, link().trakt_tv_trending % link().trakt_key)
        except: return
        index().showList(self.list[:100])

    def trakt_collection(self):
        self.list = self.trakt_list(link().trakt_tv_collection % (link().trakt_key, link().trakt_user))
        index().showList(self.list)

    def trakt_watchlist(self):
        self.list = self.trakt_list(link().trakt_tv_watchlist % (link().trakt_key, link().trakt_user))
        index().showList(self.list)

    def imdb_watchlist(self):
        self.list = self.imdb_list4(link().imdb_watchlist % link().imdb_user)
        try: self.list = sorted(self.list, key=itemgetter('name'))
        except: return
        index().showList(self.list)

    def search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_tv_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().showList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url.replace(link().imdb_base, link().imdb_akas)).result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                name = common.parseDOM(show, "a")[1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.sub('[^0-9]', '', year)[:4]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1] 
                except:
                    image = link().imdb_tv_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = common.parseDOM(show, "span", attrs = { "class": "genre" })
                    genre = common.parseDOM(genre, "a")
                    genre = " / ".join(genre)
                    if genre == '': raise Exception()
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = '0'

                try:
                    plot = common.parseDOM(show, "span", attrs = { "class": "outline" })[0]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

    def imdb_list2(self, url):
        try:
            result = getUrl(url, mobile=True).result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "div", attrs = { "class": "col-xs.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "span", attrs = { "class": "h3" })[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "div", attrs = { "class": "unbold" })[0]
                if not 'series' in year.lower(): raise Exception()
                year = re.sub('[^0-9]', '', year)[:4]
                year = re.sub("\n|[(]|[)]|\s", "", year)
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = re.findall('tt(\d*)', url, re.I)[0]
                url = link().imdb_title % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_tv_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '0', 'plot': '0'})
            except:
                pass

        return self.list

    def imdb_list3(self, url):
        try:
            url = url.replace(link().imdb_base, link().imdb_akas)
            result = getUrl(url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "pagination" })[0]
                pages = re.compile('.+?\d+.+?(\d+)').findall(pages)[0]

                for i in range(1, int(pages)):
                    self.data.append('')
                    showsUrl = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    threads.append(Thread(self.thread, showsUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            shows = common.parseDOM(result, "div", attrs = { "class": "list_item.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "a", attrs = { "onclick": ".+?" })[-1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                if not 'series' in year.lower(): raise Exception()
                year = re.compile('[(](\d{4})').findall(year)[0]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_tv_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    plot = common.parseDOM(show, "div", attrs = { "class": "item_description" })[0]
                    plot = plot.rsplit('<span>', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '0', 'plot': plot})
            except:
                pass

        return self.list

    def imdb_list4(self, url):
        try:
            URL = url.replace(link().imdb_base, link().imdb_akas)
            url = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(url))
            result = getUrl(url, referer=url).result

            try:
                threads = []
                pages = common.parseDOM(result, "div", attrs = { "class": "desc" })
                pages = [re.compile('of (\d+) titles').findall(i)[0] for i in pages][0]
                pages = (int(pages)+100)/100
                for i in range(1, int(pages)):
                    self.data.append('')
                    showsUrl = URL.replace('&page=1', '&page=%s' % str(i+1))
                    showsUrl = 'http://9proxy.in/b.php?u=%s&b=28' % urllib.quote_plus(urllib.unquote_plus(showsUrl))
                    threads.append(Thread(self.thread, showsUrl, i-1))
                [i.start() for i in threads]
                [i.join() for i in threads]
                for i in self.data: result += i
            except:
                pass

            result = result.replace('\n','')
            shows = common.parseDOM(result, "div", attrs = { "class": "lister-item mode-detail" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "h3", attrs = { "class": "lister-item-header" })[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "lister-item-year.+?" })[0]
                year = re.compile('[(](.+?)[)]').findall(year)[-1]
                if year.isdigit(): raise Exception()
                year = re.compile('(\d{4}).+').findall(year)[0]
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = common.parseDOM(show, "img", ret="data-tconst")[0]
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    image = urllib.unquote_plus(image)
                    image = image[image.find('?') + 1:].split('&')
                    image = [i.split('=', 1)[-1] for i in image if i.startswith('u=')][0]
                    image = 'http' + image.split('http' , 1)[-1]
                    if not ('_SX' in image or '_SY' in image): raise Exception()
                    image = image.rsplit('_SX', 1)[0].rsplit('_SY', 1)[0] + '_SX500.' + image.rsplit('.', 1)[-1]
                except:
                    image = link().imdb_image
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    plot = common.parseDOM(show, "p", attrs = { "class": "" })[0]
                    plot = plot.rsplit('<span>', 1)[0].rsplit('<a href', 1)[0].strip()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '0', 'plot': plot})
            except:
                pass

        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post).result
            result = json.loads(result)

            shows = []
            try: result = result['items']
            except: pass
            for i in result:
                try: shows.append(i['show'])
                except: pass
            if shows == []: 
                shows = result
        except:
            return

        for show in shows:
            try:
                name = show['title']
                name = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', name)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = show['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                if int(year) > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y")): raise Exception()

                imdb = show['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: image = show['images']['poster']
                except: image = show['poster']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = show['genres']
                    genre = " / ".join(genre)
                    if genre == '': raise Exception()
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = '0'

                try:
                    plot = show['overview']
                    if plot == '': raise Exception()
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = '0'

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url, referer=url).result
            self.data[i] = result
        except:
            return

class seasons:
    def __init__(self):
        self.list = []

    def get(self, url, year, imdb, image, genre, plot, show, show_alt='', tvdb='', idx=True):
        if idx == True:
            #self.list = self.tvdb_list(url, year, imdb, tvdb, image, genre, plot, show, show_alt)
            try: self.list = cache2(self.tvdb_list, url, year, imdb, tvdb, image, genre, plot, show, show_alt)
            except: return
            index().seasonList(self.list)
        else:
            self.list = self.tvdb_list(url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx=False)
            return self.list

    def tvdb_list(self, url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx=True):
        try:
            if (tvdb == '' or show_alt == ''):
                tvdb, show_alt= apiSearch().imdb_to_tvdb(show, year, imdb)

            tvdbUrl = link().tvdb_episodes % (link().tvdb_key, tvdb)
            result = getUrl(tvdbUrl).result

            genre = common.parseDOM(result, "Genre")[0]
            genre = [i for i in genre.split('|') if not i == '']
            genre = " / ".join(genre)
            if genre == '': genre = '0'
            genre = common.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            poster = common.parseDOM(result, "poster")[0]
            if not poster == '': poster = link().tvdb_poster + poster
            else: poster = image
            poster = common.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: desc = common.parseDOM(result, "Overview")[0]
            except: desc = plot
            if desc == '': desc = plot
            desc = desc.replace('\n','')
            desc = common.replaceHTMLCodes(desc)
            desc = desc.encode('utf-8')

            networks = ['BBC One', 'BBC Two', 'BBC Three', 'BBC Four', 'CBBC', 'CBeebies', 'ITV', 'ITV1', 'ITV2', 'ITV3', 'ITV4', 'Channel 4', 'E4', 'More4', 'Channel 5', 'Sky1']
            try: network = common.parseDOM(result, "Network")[0]
            except:  network = ''
            if network in networks: country = 'UK'
            else: country = 'US'
            dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
            if country == 'UK': dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 0)

            seasons = common.parseDOM(result, "Episode")
            seasons = [i for i in seasons if common.parseDOM(i, "EpisodeNumber")[0] == '1']
            seasons = [i for i in seasons if not common.parseDOM(i, "SeasonNumber")[0] == '0']
        except:
            return

        for season in seasons:
            try:
                date = common.parseDOM(season, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int(dt.strftime("%Y%m%d%H%M")): raise Exception()

                num = common.parseDOM(season, "SeasonNumber")[0]
                num = '%01d' % int(num)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': poster, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': desc, 'show': show, 'show_alt': show_alt, 'season': num, 'sort': '%10d' % int(num), 'idx_data': ''})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        if not idx == True:
            for i in range(0, len(self.list)): self.list[i].update({'idx_data': result})
        return self.list

class episodes:
    def __init__(self):
        self.list = []
        self.data = []

    def get(self, name, url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx_data='', idx=True):
        if idx == True:
            #self.list = self.tvdb_list(name, url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx_data)
            try: self.list = cache(self.tvdb_list, name, url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx_data)
            except: return
            index().episodeList(self.list)
        else:
            self.list = self.tvdb_list(name, url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx_data)
            return self.list

    def get2(self, url):
        if url.startswith(link().scn_base):
            #self.list = self.scn_list(url)
            try: self.list = cache(self.scn_list, url)
            except: return
        index().episodeList(self.list)

    def calendar(self, url):
        date = url
        url = link().trakt_tv_calendar % (link().trakt_key, re.sub('[^0-9]', '', str(date)), '1')
        #self.list = self.trakt_list(url)
        try: self.list = cache2(self.trakt_list, url)
        except: return
        self.list = sorted(self.list, key=itemgetter('name'))
        index().episodeList(self.list)

    def added(self):
        if not (link().trakt_user == '' or link().trakt_password == '') and getSetting("trakt_episodes") == 'true':
            now = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
            date = datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=30)
            url = link().trakt_tv_user_calendar % (link().trakt_key, link().trakt_user, re.sub('[^0-9]', '', str(date)), '31')
            self.list = self.trakt_list(url)
            try: self.list = self.list[::-1]
            except: return
            index().episodeList(self.list)
        else:
            #self.list = self.scn_list(link().scn_tv_added)
            try: self.list = cache(self.scn_list, link().scn_tv_added)
            except: return
            index().episodeList(self.list)

    def tvdb_list(self, name, url, year, imdb, tvdb, image, genre, plot, show, show_alt, idx_data):
        try:
            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            tvdbUrl = link().tvdb_episodes % (link().tvdb_key, tvdb)
            if not idx_data == '': result = idx_data
            else: result = getUrl(tvdbUrl).result

            fanart = common.parseDOM(result, "fanart")[0]

            networks = ['BBC One', 'BBC Two', 'BBC Three', 'BBC Four', 'CBBC', 'CBeebies', 'ITV', 'ITV1', 'ITV2', 'ITV3', 'ITV4', 'Channel 4', 'E4', 'More4', 'Channel 5', 'Sky1']
            try: network = common.parseDOM(result, "Network")[0]
            except:  network = ''
            if network in networks: country = 'UK'
            else: country = 'US'
            dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 5)
            if country == 'UK': dt = datetime.datetime.utcnow() - datetime.timedelta(hours = 0)

            episodes = common.parseDOM(result, "Episode")
            episodes = [i for i in episodes if '%01d' % int(common.parseDOM(i, "SeasonNumber")[0]) == season]
            episodes = [i for i in episodes if not common.parseDOM(i, "EpisodeNumber")[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if date == '' or '-00' in date: raise Exception()
                if int(re.sub('[^0-9]', '', str(date)) + '0000') + 10500 > int(dt.strftime("%Y%m%d%H%M")): raise Exception()

                title = common.parseDOM(episode, "EpisodeName")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "EpisodeNumber")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                thumb = common.parseDOM(episode, "filename")[0]
                if not thumb == '': thumb = link().tvdb_thumb + thumb
                elif not fanart == '': thumb = link().tvdb_thumb + fanart
                else: thumb = image
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                try: desc = common.parseDOM(episode, "Overview")[0]
                except: desc = plot
                if desc == '': desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'tvrage': '0', 'season': season, 'episode': num, 'show': show, 'show_alt': show_alt, 'url': url, 'image': thumb, 'date': date, 'genre': genre, 'plot': desc, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def trakt_list(self, url):
        try:
            post = urllib.urlencode({'username': link().trakt_user, 'password': link().trakt_password})

            result = getUrl(url, post=post).result
            episodes = json.loads(result)
        except:
            return

        for i in episodes:
            try:
                date = i['date']
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                for episode in i['episodes']:
                    try:
                        title = episode['episode']['title']
                        if title == '': raise Exception()
                        title = common.replaceHTMLCodes(title)
                        title = title.encode('utf-8')

                        season = episode['episode']['season']
                        season = re.sub('[^0-9]', '', '%01d' % int(season))
                        if season == '0': raise Exception()
                        season = season.encode('utf-8')

                        num = episode['episode']['number']
                        num = re.sub('[^0-9]', '', '%01d' % int(num))
                        if num == '0': raise Exception()
                        num = num.encode('utf-8')

                        show = episode['show']['title']
                        if show == '': raise Exception()
                        show = common.replaceHTMLCodes(show)
                        show = show.encode('utf-8')

                        show_alt = show

                        name = show + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                        try: name = name.encode('utf-8')
                        except: pass

                        year = episode['show']['year']
                        year = re.sub('[^0-9]', '', str(year))
                        year = year.encode('utf-8')

                        imdb = episode['show']['imdb_id']
                        imdb = re.sub('[^0-9]', '', str(imdb))
                        if imdb == '': raise Exception()
                        imdb = imdb.encode('utf-8')

                        url = link().trakt_base
                        url = common.replaceHTMLCodes(url)
                        url = url.encode('utf-8')

                        tvdb = episode['show']['tvdb_id']
                        tvdb = re.sub('[^0-9]', '', str(tvdb))
                        if tvdb == '': tvdb = '0'
                        tvdb = tvdb.encode('utf-8')

                        thumb = episode['episode']['images']['screen']
                        if thumb == '': thumb = episode['show']['images']['poster']
                        if thumb == '': thumb = link().imdb_tv_image
                        thumb = common.replaceHTMLCodes(thumb)
                        thumb = thumb.encode('utf-8')

                        try:
                            genre = episode['show']['genres']
                            genre = " / ".join(genre)
                            if genre == '': raise Exception()
                            genre = common.replaceHTMLCodes(genre)
                            genre = genre.encode('utf-8')
                        except:
                            genre = '0'

                        try:
                            desc = episode['episode']['overview']
                            if desc == '': desc = episode['show']['overview']
                            if desc == '': raise Exception()
                            desc = common.replaceHTMLCodes(desc)
                            desc = desc.encode('utf-8')
                        except:
                            desc = '0'

                        self.list.append({'name': name, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'tvrage': '0', 'season': season, 'episode': num, 'show': show, 'show_alt': show_alt, 'url': url, 'image': thumb, 'date': date, 'genre': genre, 'plot': desc, 'sort': '%10d' % int(num)})
                    except:
                        pass
            except:
                pass

        return self.list

    def scn_list(self, url):
        try:
            param = re.compile('(.+?/page/)(\d+)').findall(url)[0]

            threads = []
            for i in range(0, 3):
                self.data.append('')
                episodesUrl = param[0] + str(i+int(param[1])) + '/'
                threads.append(Thread(self.thread, episodesUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            result = ''
            for i in self.data: result += i

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')

            episodes = common.parseDOM(result, "div", attrs = { "class": "post" })
        except:
            return

        try:
            next = common.parseDOM(self.data[-1], "link", ret="href", attrs = { "rel": "next" })[0]
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for episode in episodes:
            try:
                dt = str(datetime.datetime.utcnow().year)
                try: date = re.compile('>Aired:(.+?)<').findall(episode)[0]
                except: date = dt
                date = date.strip()
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if not date.startswith(dt): raise Exception()

                title = common.parseDOM(episode, "div", attrs = { "class": "storycontent" })[0]
                title = common.parseDOM(title, "strong")[0]
                title = title.replace("&#8216;", "'").replace("&#8217;", "'").replace("&#8211;", '-').replace("&#8230;", '.')
                title = common.replaceHTMLCodes(title)
                title = unicode(title.encode('utf-8'), 'ascii', 'ignore')
                title = title.encode('utf-8')

                season = common.parseDOM(episode, "a", attrs = { "rel": "bookmark" })[0]
                season = re.compile('.* S(\d+?)E\d+? ').findall(season)[0]
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0': raise Exception()
                season = season.encode('utf-8')

                num = common.parseDOM(episode, "a", attrs = { "rel": "bookmark" })[0]
                num = re.compile('.* S\d+?E(\d+?) ').findall(num)[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                if num == '0': raise Exception()
                num = num.encode('utf-8')

                show = common.parseDOM(episode, "a", attrs = { "rel": "bookmark" })[0]
                show = re.compile('(.*) S\d+?E\d+? ').findall(show)[0]
                show = show.replace("&#8216;", "'").replace("&#8217;", "'").replace("&#8211;", '-').replace("&#8230;", '.')
                show = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', show)
                show = common.replaceHTMLCodes(show)
                show = unicode(show.encode('utf-8'), 'ascii', 'ignore')
                show = show.encode('utf-8')

                name = show + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                try: name = name.encode('utf-8')
                except: pass

                tvrage = common.parseDOM(episode, "a", ret="href", attrs = { "class": "info_link" })
                tvrage = [i for i in tvrage if 'tvrage' in i][0]
                tvrage = common.replaceHTMLCodes(tvrage)
                tvrage = tvrage.encode('utf-8')

                thumb = link().imdb_tv_image
                try: thumb = common.parseDOM(episode, "img", ret="src")[0]
                except: pass
                try: thumb = common.parseDOM(episode, "img", ret="src", attrs = { "width": "696px" })[0]
                except: pass
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                try:
                    desc = common.parseDOM(episode, "div", attrs = { "class": "storycontent" })[0]
                    desc = desc.split('</em>', 1)[-1]
                    desc = desc.split('>', 1)[-1].split('<', 1)[0]
                    if desc == '': raise Exception()
                    desc = desc.replace("&#8216;", "'").replace("&#8217;", "'").replace("&#8211;", '-').replace("&#8230;", '.')
                    desc = common.replaceHTMLCodes(desc)
                    desc = unicode(desc.encode('utf-8'), 'ascii', 'ignore')
                    desc = desc.encode('utf-8')
                except:
                    desc = '0'

                self.list.append({'name': name, 'title': title, 'year': '0', 'imdb': '0', 'tvdb': '0', 'tvrage': tvrage, 'season': season, 'episode': num, 'show': show, 'show_alt': show, 'url': '0', 'image': thumb, 'date': date, 'genre': '0', 'plot': desc, 'next': next})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url, referer=url).result
            self.data[i] = result
        except:
            return

class apiSearch:
    def imdb_to_tvdb(self, show, year, imdb):
        tvdb, show_alt = '0', show.encode('utf-8')

        try:
            result = getUrl(link().tvdb_search % imdb).result
            result = common.parseDOM(result, "Series")
            if len(result) == 0:
                result = getUrl(link().tvdb_search2 % urllib.quote_plus(show)).result
                result = common.parseDOM(result, "Series")
                result = [i for i in result if self.cleantitle_tv(show) == self.cleantitle_tv(common.replaceHTMLCodes(common.parseDOM(i, "SeriesName")[0])) and any(x in common.parseDOM(i, "FirstAired")[0] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]

            show_alt = common.parseDOM(result, "SeriesName")[0]
            show_alt = common.replaceHTMLCodes(show_alt)
            show_alt = show_alt.encode('utf-8')
            tvdb = common.parseDOM(result, "seriesid")[0]
            tvdb = str(tvdb).encode('utf-8')
        except:
            pass

        return (tvdb, show_alt)

    def tvdb_to_tvrage(self, title, year, tvdb, season, episode, show, date, genre):
        try:
            exception = True
            if len(season) > 3: exception = False
            genre = [i.strip() for i in genre.split('/')]
            genre = [i for i in genre if any(x == i for x in ['Reality', 'Game Show', 'Talk Show'])]
            if not len(genre) == 0: exception = False
            blocks = ['73141']
            if tvdb in blocks: exception = False
            if exception == True: raise Exception()
        except:
            return (season, episode)

        try:
            tvrage = '0'
            result = getUrl(link().trakt_tv_search % (link().trakt_key, tvdb)).result
            result = json.loads(result)
            tvrage = result['tvrage_id']
            tvrage = str(tvrage)
        except:
            pass

        try:
            if not tvrage == '0': raise Exception()
            result = getUrl(link().tvrage_search2 % urllib.quote_plus(show)).result
            result = common.parseDOM(result, "show")
            result = [i for i in result if self.cleantitle_tv(show) == self.cleantitle_tv(common.replaceHTMLCodes(common.parseDOM(i, "name")[0])) and any(x in common.parseDOM(i, "started")[0] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            tvrage = common.parseDOM(result, "showid")[0]
            tvrage = str(tvrage)
        except:
            pass

        try:
            if tvrage == '0': raise Exception()
            result = getUrl(link().epguides_info % tvrage).result
            search = re.compile('\d+?,(\d+?),(\d+?),.+?,(\d+?/.+?/\d+?),"(.+?)",.+?,".+?"').findall(result)
            d = '%02d/%s/%s' % (int(date.split('-')[2]), {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}[date.split('-')[1]], date.split('-')[0][-2:])
            match = [i for i in search if self.cleantitle_tv(title) == self.cleantitle_tv(i[3])]
            match += [i for i in search if d == i[2]]
            season = str('%01d' % int(match[0][0]))
            episode = str('%01d' % int(match[0][1]))
            return (season, episode)
        except:
            pass

        try:
            if tvrage == '0': raise Exception()
            result = getUrl(link().tvrage_info % tvrage).result
            search = re.compile('<td.+?><a.+?title=.+?season.+?episode.+?>(\d+?)x(\d+?)<.+?<td.+?>(\d+?/.+?/\d+?)<.+?<td.+?>.+?href=.+?>(.+?)<').findall(result.replace('\n',''))
            d = '%02d/%s/%s' % (int(date.split('-')[2]), {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}[date.split('-')[1]], date.split('-')[0])
            match = [i for i in search if self.cleantitle_tv(title) == self.cleantitle_tv(i[3])]
            match += [i for i in search if d == i[2]]
            season = str('%01d' % int(match[0][0]))
            episode = str('%01d' % int(match[0][1]))
            return (season, episode)
        except:
            pass

        return (season, episode)

    def tvrage_to_imdb(self, tvrage):
        show, show_alt, year, imdb, tvdb = '0', '0', '0', '0', '0'

        try:
            search = re.compile('/id-(\d+)').findall(tvrage)
            if len(search) == 0:
                result = getUrl(tvrage.replace('https://', 'http://'), timeout='20').result
                search = re.compile('[?]sid=(\d+)').findall(result)
                search += re.compile('[?]apply_for=\d+_(\d+)').findall(result)
            result = getUrl(link().tvrage_search % str(search[0]), timeout='20').result

            year = common.parseDOM(result, "started")[0]
            year = re.compile('(\d{4})').findall(year)[0]
            year = str(year).encode('utf-8')
            show = common.parseDOM(result, "showname")[0]
            show = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', show)
            show = common.replaceHTMLCodes(show)
            show = show.encode('utf-8')
            aka = re.compile('<aka>(.+?)</aka>').findall(result)
            aka += common.parseDOM(result, "aka", attrs = { "attr": "Short title" })
            aka += common.parseDOM(result, "aka", attrs = { "country": "US" })
            try: aka = aka[0]
            except: aka = None
            aka = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', aka)
            aka = common.replaceHTMLCodes(aka)
            aka = aka.encode('utf-8')
        except:
            pass

        try:
            result = getUrl(link().tvdb_search2 % urllib.quote_plus(show)).result
            result = common.parseDOM(result, "Series")
            if len(result) == 0:
                result = getUrl(link().tvdb_search2 % urllib.quote_plus(aka)).result
                result = common.parseDOM(result, "Series")
                show = aka
            result = [i for i in result if self.cleantitle_tv(show) == self.cleantitle_tv(common.replaceHTMLCodes(common.parseDOM(i, "SeriesName")[0])) and any(x in common.parseDOM(i, "FirstAired")[0] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            show_alt = common.parseDOM(result, "SeriesName")[0]
            show_alt = common.replaceHTMLCodes(show_alt)
            show_alt = show_alt.encode('utf-8')
            tvdb = common.parseDOM(result, "seriesid")[0]
            tvdb = str(tvdb).encode('utf-8')
            imdb = common.parseDOM(result, "IMDB_ID")[0]
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = str(imdb).encode('utf-8')
        except:
            pass

        try:
            if not imdb == '0': raise Exception()
            result = getUrl(link().imdb_api_search % urllib.quote_plus(show)).result
            result = json.loads(result)
            match = []
            for i in result.keys(): match += result[i]
            imdb = [i['id'] for i in match if show == i['title'] and year in i['description'] and 'series' in i['description']][0]
            imdb = re.sub('[^0-9]', '', str(imdb))
            imdb = str(imdb).encode('utf-8')
        except:
            pass

        return (show, show_alt, year, imdb, tvdb)

    def cleantitle_movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

class trailer:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url is None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url is None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url is None: return
            return url

    def youtube_search(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url is None: return url
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.youtube_info % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.youtube_watch % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return


class resolver:
    def __init__(self):
        self.sources_dict()
        self.sources = []

    def get_host(self, name, title, year, imdb, url, image, genre, plot, tvdb, tvrage, date, show, show_alt, season, episode):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            if content == 'movie':
                self.sources = self.sources_movie(name, title, year, imdb, self.hostDict)
            else:
                if imdb == '0' and 'tvrage.com' in tvrage:
                    show, show_alt, year, imdb, tvdb = apiSearch().tvrage_to_imdb(tvrage)
                    if imdb == '0': raise Exception()
                season, episode = apiSearch().tvdb_to_tvrage(title, year, tvdb, season, episode, show, date, genre)
                self.sources = self.sources_tv(name, title, year, imdb, tvdb, season, episode, show, show_alt, self.hostDict)

            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            for i in range(0,len(self.sources)):
                self.sources[i].update({'name': name, 'image': image, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': episode})

            if content == 'movie': 
                index().moviesourceList(self.sources)
            else: 
                index().tvsourceList(self.sources)
        except:
            index().infoDialog(language(30314).encode("utf-8"))
            return

    def play_host(self, content, name, url, imdb, source, provider):
        try:
            url = self.sources_resolve(url, provider)
            if url is None: raise Exception()

            if getSetting("playback_info") == 'true':
                index().infoDialog(source, header=name)

            player().run(content, name, url, imdb)
            return url
        except:
            index().infoDialog(language(30314).encode("utf-8"))
            return

    def run(self, name, title, year, imdb, tvdb, tvrage, season, episode, show, show_alt, date, genre, url):
        try:
            if show == None: content = 'movie'
            else: content = 'episode'

            if content == 'movie':
                self.sources = self.sources_movie(name, title, year, imdb, self.hostDict)
            else:
                if imdb == '0' and 'tvrage.com' in tvrage:
                    show, show_alt, year, imdb, tvdb = apiSearch().tvrage_to_imdb(tvrage)
                    if imdb == '0': raise Exception()
                season, episode = apiSearch().tvdb_to_tvrage(title, year, tvdb, season, episode, show, date, genre)
                self.sources = self.sources_tv(name, title, year, imdb, tvdb, season, episode, show, show_alt, self.hostDict)

            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            autoplay = getSetting("autoplay")
            if PseudoTV == 'True': autoplay = 'true'
            elif not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
                autoplay = getSetting("autoplay_library")

            if url == 'dialog://':
                url = self.sources_dialog()
            elif url == 'direct://':
                url = self.sources_direct()
            elif not autoplay == 'true':
                url = self.sources_dialog()
            else:
                url = self.sources_direct()

            if url is None: raise Exception()
            if url == 'close://': return

            if getSetting("playback_info") == 'true':
                index().infoDialog(self.selectedSource, header=name)

            player().run(content, name, url, imdb)
            return url
        except:
            if not PseudoTV == 'True': return
            index().infoDialog(language(30314).encode("utf-8"))
            return

    def cleantitle_movie(self, title):
        title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def cleantitle_tv(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def sources_movie(self, name, title, year, imdb, hostDict):
        threads = []

        global icefilms_sources
        icefilms_sources = []
        if getSetting("icefilms") == 'true':
            threads.append(Thread(icefilms().mv, name, title, year, imdb, hostDict))

        global primewire_sources
        primewire_sources = []
        if getSetting("primewire") == 'true':
            threads.append(Thread(primewire().mv, name, title, year, imdb, hostDict))

        global movie25_sources
        movie25_sources = []
        if getSetting("movie25") == 'true':
            threads.append(Thread(movie25().mv, name, title, year, imdb, hostDict))

        global flixanity_sources
        flixanity_sources = []
        if getSetting("flixanity") == 'true':
            threads.append(Thread(flixanity().mv, name, title, year, imdb, hostDict))

        global movieshd_sources
        movieshd_sources = []
        if getSetting("movieshd") == 'true':
            threads.append(Thread(movieshd().mv, name, title, year, imdb, hostDict))

        global muchmovies_sources
        muchmovies_sources = []
        if getSetting("muchmovies") == 'true':
            threads.append(Thread(muchmovies().mv, name, title, year, imdb, hostDict))

        global glowgaze_sources
        glowgaze_sources = []
        if getSetting("glowgaze") == 'true':
            threads.append(Thread(glowgaze().mv, name, title, year, imdb, hostDict))

        global movietube_sources
        movietube_sources = []
        if getSetting("movietube") == 'true':
            threads.append(Thread(movietube().mv, name, title, year, imdb, hostDict))

        global yify_sources
        yify_sources = []
        if getSetting("yify") == 'true':
            threads.append(Thread(yify().mv, name, title, year, imdb, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox") == 'true':
            threads.append(Thread(vkbox().mv, name, title, year, imdb, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd") == 'true':
            threads.append(Thread(istreamhd().mv, name, title, year, imdb, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies") == 'true':
            threads.append(Thread(simplymovies().mv, name, title, year, imdb, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm") == 'true':
            threads.append(Thread(moviestorm().mv, name, title, year, imdb, hostDict))

        global noobroom_sources
        noobroom_sources = []
        if getSetting("noobroom") == 'true':
            threads.append(Thread(noobroom().mv, name, title, year, imdb, hostDict))

        global einthusan_sources
        einthusan_sources = []
        if getSetting("einthusan") == 'true':
            threads.append(Thread(einthusan().mv, name, title, year, imdb, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = icefilms_sources + primewire_sources + movie25_sources + flixanity_sources + movieshd_sources + muchmovies_sources + glowgaze_sources + movietube_sources + yify_sources + vkbox_sources + istreamhd_sources + simplymovies_sources + moviestorm_sources + noobroom_sources + einthusan_sources

        return self.sources

    def sources_tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        threads = []

        global icefilms_sources
        icefilms_sources = []
        if getSetting("icefilms_tv") == 'true':
            threads.append(Thread(icefilms().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global primewire_sources
        primewire_sources = []
        if getSetting("primewire_tv") == 'true':
            threads.append(Thread(primewire().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global watchseries_sources
        watchseries_sources = []
        if getSetting("watchseries_tv") == 'true':
            threads.append(Thread(watchseries().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global flixanity_sources
        flixanity_sources = []
        if getSetting("flixanity_tv") == 'true':
            threads.append(Thread(flixanity().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global shush_sources
        shush_sources = []
        if getSetting("shush_tv") == 'true':
            threads.append(Thread(shush().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global ororo_sources
        ororo_sources = []
        if getSetting("ororo_tv") == 'true':
            threads.append(Thread(ororo().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global putlockertv_sources
        putlockertv_sources = []
        if getSetting("putlocker_tv") == 'true':
            threads.append(Thread(putlockertv().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global clickplay_sources
        clickplay_sources = []
        if getSetting("clickplay_tv") == 'true':
            threads.append(Thread(clickplay().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox_tv") == 'true':
            threads.append(Thread(vkbox().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd_tv") == 'true':
            threads.append(Thread(istreamhd().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies_tv") == 'true':
            threads.append(Thread(simplymovies().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm_tv") == 'true':
            threads.append(Thread(moviestorm().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        global noobroom_sources
        noobroom_sources = []
        if getSetting("noobroom_tv") == 'true':
            threads.append(Thread(noobroom().tv, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = icefilms_sources + primewire_sources + watchseries_sources + flixanity_sources + shush_sources + ororo_sources + putlockertv_sources + vkbox_sources + clickplay_sources + istreamhd_sources + simplymovies_sources + moviestorm_sources + noobroom_sources

        return self.sources

    def sources_resolve(self, url, provider):
        try:
            if provider == 'Icefilms': url = icefilms().resolve(url)
            elif provider == 'Primewire': url = primewire().resolve(url)
            elif provider == 'Movie25': url = movie25().resolve(url)
            elif provider == 'Watchseries': url = watchseries().resolve(url)
            elif provider == 'Flixanity': url = flixanity().resolve(url)
            elif provider == 'MoviesHD': url = movieshd().resolve(url)
            elif provider == 'Muchmovies': url = muchmovies().resolve(url)
            elif provider == 'Glowgaze': url = glowgaze().resolve(url)
            elif provider == 'Movietube': url = movietube().resolve(url)
            elif provider == 'YIFY': url = yify().resolve(url)
            elif provider == 'Shush': url = shush().resolve(url)
            elif provider == 'Ororo': url = ororo().resolve(url)
            elif provider == 'PutlockerTV': url = putlockertv().resolve(url)
            elif provider == 'Clickplay': url = clickplay().resolve(url)
            elif provider == 'VKBox': url = vkbox().resolve(url)
            elif provider == 'iStreamHD': url = istreamhd().resolve(url)
            elif provider == 'Simplymovies': url = simplymovies().resolve(url)
            elif provider == 'Moviestorm': url = moviestorm().resolve(url)
            elif provider == 'Noobroom': url = noobroom().resolve(url)
            elif provider == 'Einthusan': url = einthusan().resolve(url)
            return url
        except:
            return

    def sources_filter(self):
        #hd_rank = ['VK', 'MoviesHD', 'Muchmovies', 'Shush', 'Glowgaze', 'Movietube', 'YIFY', 'Noobroom', 'Firedrive', 'Movreel', 'Billionuploads', '180upload', 'Hugefiles', 'Einthusan']
        #sd_rank = ['Ororo', 'Glowgaze', 'Noobroom', 'Firedrive', 'Putlocker', 'Sockshare', 'iShared', 'Mailru', 'VK', 'Movreel', 'Played', 'Promptfile', 'Mightyupload', 'Gorillavid', 'Bestreams', 'Divxstage', 'Flashx', 'Vidbull', 'Daclips', 'Sharesix']
        hd_rank = [getSetting("hosthd1"), getSetting("hosthd2"), getSetting("hosthd3"), getSetting("hosthd4"), getSetting("hosthd5"), getSetting("hosthd6"), getSetting("hosthd7"), getSetting("hosthd8"), getSetting("hosthd9"), getSetting("hosthd10"), getSetting("hosthd11"), getSetting("hosthd12"), getSetting("hosthd13"), getSetting("hosthd14")]
        sd_rank = [getSetting("host1"), getSetting("host2"), getSetting("host3"), getSetting("host4"), getSetting("host5"), getSetting("host6"), getSetting("host7"), getSetting("host8"), getSetting("host9"), getSetting("host10"), getSetting("host11"), getSetting("host12"), getSetting("host13"), getSetting("host14"), getSetting("host15"), getSetting("host16"), getSetting("host17"), getSetting("host18"), getSetting("host19"), getSetting("host20")]

        for i in range(len(self.sources)): self.sources[i]['source'] = self.sources[i]['source'].lower()
        self.sources = sorted(self.sources, key=itemgetter('source'))

        filter = []
        for host in hd_rank: filter += [i for i in self.sources if i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        for host in sd_rank: filter += [i for i in self.sources if not i['quality'] == 'HD' and i['source'].lower() == host.lower()]
        filter += [i for i in self.sources if not i['quality'] == 'HD' and not any(x == i['source'].lower() for x in [r.lower() for r in sd_rank])]
        self.sources = filter

        filter = []
        filter += [i for i in self.sources if i['quality'] == 'HD']
        filter += [i for i in self.sources if i['quality'] == 'SD']
        filter += [i for i in self.sources if i['quality'] == 'SCR']
        filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        if getSetting("play_hd") == 'false':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        count = 1
        for i in range(len(self.sources)):
            self.sources[i]['host'] = self.sources[i]['source']
            self.sources[i]['source'] = str('%02d' % count) + ' | [B]' + self.sources[i]['provider'].upper() + '[/B] | ' + self.sources[i]['source'].upper() + ' | ' + self.sources[i]['quality']
            count = count + 1

        return self.sources

    def sources_dialog(self):
        try:
            sourceList, urlList, providerList = [], [], []

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select]['source']
            return url
        except:
            return

    def sources_direct(self):
        hd_blocks = ['Muchmovies', 'Firedrive', 'Movreel', 'Billionuploads', '180upload', 'Hugefiles']
        hd_blocks = [i.lower() for i in hd_blocks]

        if not (getSetting("realdedrid_user") == '' or getSetting("realdedrid_password") == ''):
            try:
                filter = []
                rd_hosts = getUrl('https://real-debrid.com/api/hosters.php').result
                rd_hosts = [i.split('.')[0].replace('"', '').lower() for i in rd_hosts.split(',')]
                filter += [i for i in self.sources if i['quality'] == 'HD' and i['host'] in rd_hosts]
                filter += [i for i in self.sources if i['quality'] == 'HD' and not i['host'] in hd_blocks]
                filter += [i for i in self.sources if not i['quality'] == 'HD' and i['host'] in rd_hosts]
                filter += [i for i in self.sources if not i['quality'] == 'HD' and not i['host'] in rd_hosts]
                self.sources = filter
            except:
                pass
        else:
            self.sources = [i for i in self.sources if not i['host'] in hd_blocks]

        if getSetting("autoplay_hd") == 'false':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        u = None

        for i in self.sources:
            try:
                url = self.sources_resolve(i['url'], i['provider'])
                xbmc.sleep(1000)
                if url == None: raise Exception()
                if u == None: u = url

                if url.startswith('http://'):
                    request = urllib2.Request(url.rsplit('|', 1)[0])
                    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
                    request.add_header('Cookie', 'video=true')
                    response = urllib2.urlopen(request, timeout=20)
                    chunk = response.read(16 * 1024)
                    response.close()
                    if 'text/html' in str(response.info()["Content-Type"]): raise Exception()

                self.selectedSource = i['source']
                return url
            except:
                pass

        return u

    def sources_dict(self):
        self.hostDict = [
        '2gb-hosting',
        'allmyvideos',
        #'180upload',
        'bayfiles',
        'bestreams',
        #'billionuploads',
        'castamp',
        #'clicktoview',
        'daclips',
        'divxstage',
        'donevideo',
        'ecostream',
        'filenuke',
        'firedrive',
        'flashx',
        'gorillavid',
        'hostingbulk',
        #'hugefiles',
        'ishared',
        'jumbofiles',
        'lemuploads',
        'limevideo',
        #'megarelease',
        'mightyupload',
        'movdivx',
        'movpod',
        'movreel',
        'movshare',
        'movzap',
        'muchshare',
        'nosvideo',
        'novamov',
        'nowvideo',
        'played',
        'playwire',
        'primeshare',
        'promptfile',
        'purevid',
        'putlocker',
        'sharerepo',
        'sharesix',
        'sockshare',
        'stagevu',
        'streamcloud',
        'thefile',
        'uploadc',
        'vidbull',
        'videobb',
        'videoweed',
        'videozed',
        #'vidhog',
        #'vidplay',
        'vidx',
        #'vidxden',
        #'watchfreeinhd',
        'xvidstage',
        'youtube',
        'yourupload',
        'youwatch',
        'zalaa'
        ]


class icefilms:
    def __init__(self):
        global icefilms_sources
        icefilms_sources = []
        self.base_link = 'http://www.icefilms.info'
        self.moviesearch_link = 'http://www.icefilms.info/movies/a-z/%s'
        self.tvsearch_link = 'http://www.icefilms.info/tv/a-z/%s'
        self.video_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.php?vid=%s'
        self.post_link = 'http://www.icefilms.info/membersonly/components/com_iceplayer/video.phpAjaxResp.php'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = title.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.moviesearch_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            id = re.compile('id=%s>.+?href=/ip.php[?]v=(.+?)&' % imdb).findall(result)[0]
            url = self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    hosts = ['movreel', 'billionuploads', '180upload', 'hugefiles']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>DVD Screener<' in i]
                if len(sd_links) == 0: sd_links = [i for i in links if '>R5/R6 DVDRip<' in i]
                sd_links = sd_links[0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    hosts = ['movreel']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = show.upper()
            if query.startswith('THE '): query = query.replace('THE ', '')
            elif query.startswith('A '): query = query.replace('A ', '')
            if not query[0].isalpha(): query = '1'
            query = self.tvsearch_link % query[0]

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = re.compile('id=%s>.+?href=(.+?)>' % imdb).findall(result)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            id = re.compile('href=/ip.php[?]v=(.+?)&>%01dx%02d' % (int(season), int(episode))).findall(result)[0]
            id = id.split('v=')[-1]
            url = self.video_link % id
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            sec = re.compile('lastChild[.]value="(.+?)"').findall(result)[0]
            links = common.parseDOM(result, "div", attrs = { "class": "ripdiv" })

            import random

            try:
                hd_links = ''
                hd_links = [i for i in links if '>HD 720p<' in i][0]
                hd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(hd_links)
            except:
                pass

            for url, host in hd_links:
                try:
                    hosts = ['movreel', 'billionuploads', '180upload', 'hugefiles']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'HD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass

            try:
                sd_links = ''
                sd_links = [i for i in links if '>DVDRip / Standard Def<' in i][0]
                sd_links = re.compile("onclick='go[(](.+?)[)]'>Source(.+?)</a>").findall(sd_links)
            except:
                pass

            for url, host in sd_links:
                try:
                    hosts = ['movreel']
                    host = re.sub('<span\s.+?>|</span>|#\d*:','', host)
                    host = host.strip().lower()
                    if not host in hosts: raise Exception()
                    url = 'id=%s&t=%s&sec=%s&s=%s&m=%s&cap=&iqs=&url=' % (url, id, sec, random.randrange(5, 50), random.randrange(100, 300) * -1)
                    icefilms_sources.append({'source': host, 'quality': 'SD', 'provider': 'Icefilms', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(self.post_link, post=url).result
            url = result.split("?url=", 1)[-1]
            url = urllib.unquote_plus(url)

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class primewire:
    def __init__(self):
        global primewire_sources
        primewire_sources = []
        self.base_link = 'http://www.primewire.ag'
        self.key_link = 'http://www.primewire.ag/index.php?search'
        self.moviesearch_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = 'http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=2'
        self.proxy_base_link = 'http://9proxy.in'
        self.proxy_link = 'http://9proxy.in/b.php?u=%s&b=28'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            try:
                result = getUrl(self.key_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), key)
            except:
                result = getUrl(self.proxy_link % urllib.quote_plus(urllib.unquote_plus(self.key_link)), referer=self.proxy_base_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.moviesearch_link % (urllib.quote_plus(re.sub('\'', '', title)), key)
                query = self.proxy_link % urllib.quote_plus(urllib.unquote_plus(query))
                self.base_link = self.proxy_base_link

            result = getUrl(query, referer=self.base_link, close=False).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })
            result = [i for i in result if any(x in re.compile('title="Watch (.+?)"').findall(i)[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])]
            result = uniqueList(result).list

            match = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    if not i.startswith('http://'): i = '%s%s' % (self.base_link, i)
                    result = getUrl(i, referer=i).result
                    if any(x in resolver().cleantitle_movie(result) for x in [str('>' + resolver().cleantitle_movie(title) + '(%s)' % str(year) + '<')]):
                        match2 = i
                    if any(x in resolver().cleantitle_movie(result) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2
            result = getUrl(url, referer=url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = urllib.unquote_plus(url)
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    if 'primewire.ag' in url: raise Exception()
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = urllib.unquote_plus(host)
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    primewire_sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            try:
                result = getUrl(self.key_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', show)), key)
            except:
                result = getUrl(self.proxy_link % urllib.quote_plus(urllib.unquote_plus(self.key_link)), referer=self.proxy_base_link).result
                key = common.parseDOM(result, "input", ret="value", attrs = { "name": "key" })[0]
                query = self.tvsearch_link % (urllib.quote_plus(re.sub('\'', '', show)), key)
                query = self.proxy_link % urllib.quote_plus(urllib.unquote_plus(query))
                self.base_link = self.proxy_base_link

            result = getUrl(query, referer=self.base_link, close=False).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "index_item.+?" })
            result = [i for i in result if any(x in re.compile('title="Watch (.+?)"').findall(i)[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])]
            result = uniqueList(result).list

            match = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    if not i.startswith('http://'): i = '%s%s' % (self.base_link, i)
                    result = getUrl(i, referer=i).result
                    if any(x in resolver().cleantitle_tv(result) for x in [str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(year) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(year) + '<')]):
                        match2 = i
                    if any(x in resolver().cleantitle_tv(result) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            x = match2.split('primewire.ag', 1)[-1].split('&', 1)[0]
            y = x.replace('/watch-','/tv-').replace('%2Fwatch-','%2Ftv-')
            z = '/season-%01d-episode-%01d' % (int(season), int(episode))
            if y.startswith('%2F'): y += urllib.quote_plus(z)
            else: y += z
            url = match2.replace(x,y)

            result = getUrl(url, referer=url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            links = common.parseDOM(result, "tbody")

            for i in links:
                try:
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = urllib.unquote_plus(url)
                    url = re.compile('url=(.+?)&').findall(url)[0]
                    url = base64.urlsafe_b64decode(url.encode('utf-8'))
                    if 'primewire.ag' in url: raise Exception()
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = common.parseDOM(i, "a", ret="href")[0]
                    host = urllib.unquote_plus(host)
                    host = re.compile('domain=(.+?)&').findall(host)[0]
                    host = base64.urlsafe_b64decode(host.encode('utf-8'))
                    host = host.rsplit('.', 1)[0]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    host = host.encode('utf-8')

                    quality = common.parseDOM(i, "span", ret="class")[0]
                    if quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()
                    quality = quality.encode('utf-8')

                    primewire_sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class movie25:
    def __init__(self):
        global movie25_sources
        movie25_sources = []
        self.base_link = 'http://www.movie25.so'
        self.search_link = 'http://www.movie25.so/search.php?key=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % urllib.quote_plus(title)

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "movie_table" })[0]
            result = common.parseDOM(result, "li")

            match = [i for i in result if any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            match2 = [self.base_link + common.parseDOM(i, "a", ret="href")[0] for i in match]
            if match2 == []: return
            for i in match2[:10]:
                try:
                    result = getUrl(i).result
                    result = result.decode('iso-8859-1').encode('utf-8')
                    if str('tt' + imdb) in result:
                        match3 = result
                        break
                except:
                    pass

            result = common.parseDOM(match3, "div", attrs = { "class": "links_quality" })[0]

            quality = common.parseDOM(result, "h1")[0]
            quality = quality.replace('\n','').rsplit(' ', 1)[-1]
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = common.parseDOM(result, "ul")
            for i in links:
                try:
                    name = common.parseDOM(i, "a")[0]
                    name = common.replaceHTMLCodes(name)
                    if name.isdigit(): raise Exception()
                    host = common.parseDOM(i, "li", attrs = { "class": "link_name" })[0]
                    host = common.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    host = [x for x in hostDict if host.lower() == x.lower()][0]
                    url = common.parseDOM(i, "a", ret="href")[0]
                    url = '%s%s' % (self.base_link, url)
                    url = common.replaceHTMLCodes(url)
                    url = url.encode('utf-8')
                    movie25_sources.append({'source': host, 'quality': quality, 'provider': 'Movie25', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "input", ret="onclick")
            url = [i for i in url if 'location.href' in i and 'http://' in i][0]
            url = url.split("'", 1)[-1].rsplit("'", 1)[0]

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class watchseries:
    def __init__(self):
        global watchseries_sources
        watchseries_sources = []
        self.base_link = 'http://watchseries.ag'
        self.search_link = 'http://watchseries.ag/search/%s'
        self.episode_link = 'http://watchseries.ag/episode/%s_s%s_e%s.html'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.search_link % urllib.quote_plus(show)

            result = getUrl(query, referer=query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace(' (%s)' % str(int(year) - 1), ' (%s)' % year)
            result = re.compile('href="(/serie/.+?)".+?[(]%s[)]' % year).findall(result)
            result = uniqueList(result).list

            match = [self.base_link + i for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(i, referer=i).result
                    if any(x in resolver().cleantitle_tv(result) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass

            url = match2.rsplit('/', 1)[-1]
            url = self.episode_link % (url, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url, referer=url).result
            result = common.parseDOM(result, "div", attrs = { "id": "lang_1" })[0]

            for host in hostDict:
                try:
                    links = re.compile('<span>%s</span>.+?href="(.+?)"' % host.lower()).findall(result)
                    for url in links:
                        url = '%s%s' % (self.base_link, url)
                        watchseries_sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url, referer=url).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "myButton" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class flixanity:
    def __init__(self):
        global flixanity_sources
        flixanity_sources = []
        self.base_link = 'http://www.flixanity.com'
        self.moviesearch_link = 'http://www.flixanity.com/ajax/search.php?q=%s&limit=5'
        self.tvsearch_link = 'http://www.flixanity.com/ajax/search.php?q=%s&limit=5'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.moviesearch_link % urllib.quote_plus(title)

            result = getUrl(query).result
            result = json.loads(result)
            result = [i for i in result if 'Movie' in i['meta']]

            url = [i for i in result if any(x in resolver().cleantitle_movie(i['title']) for x in [resolver().cleantitle_movie(title)]) and any(x in i['title'] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == resolver().cleantitle_movie(i['title']) for x in [resolver().cleantitle_movie(title)])]
            url = url[0]['permalink']
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            result = common.parseDOM(result, "script")
            result = [i for i in result if 'var embeds' in i][0]
            result = result.replace('IFRAME', 'iframe').replace('SRC=', 'src=')
            links = common.parseDOM(result, "iframe", ret="src")
            links = [i.split('player.php?', 1)[-1] for i in links]

            for url in links:
                try:
                    host = re.compile('://(.+?)/').findall(url)[0]
                    host = host.rsplit('.', 1)[0].split('w.', 1)[-1]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]

                    flixanity_sources.append({'source': host, 'quality': 'SD', 'provider': 'Flixanity', 'url': url})
                except:
                    pass
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.tvsearch_link % urllib.quote_plus(show)

            result = getUrl(query).result
            result = json.loads(result)
            result = [i for i in result if 'TV' in i['meta']]

            url = [i for i in result if any(x in resolver().cleantitle_tv(i['title']) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)]) and any(x in i['title'] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == resolver().cleantitle_tv(i['title']) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])]
            url = url[0]['permalink']
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "item" })
            url = [i for i in url if i.endswith('season/%01d/episode/%01d' % (int(season), int(episode)))][0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "script")
            result = [i for i in result if 'var embeds' in i][0]
            result = result.replace('IFRAME', 'iframe').replace('SRC=', 'src=')
            links = common.parseDOM(result, "iframe", ret="src")
            links = [i.split('player.php?', 1)[-1] for i in links]

            for url in links:
                try:
                    host = re.compile('://(.+?)/').findall(url)[0]
                    host = host.rsplit('.', 1)[0].split('w.', 1)[-1]
                    host = [x for x in hostDict if host.lower() == x.lower()][0]

                    flixanity_sources.append({'source': host, 'quality': 'SD', 'provider': 'Flixanity', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class movieshd:
    def __init__(self):
        global movieshd_sources
        movieshd_sources = []
        self.base_link = 'http://movieshd.co'
        self.search_link = 'http://movieshd.co/?s=%s'
        self.player_link = 'http://videomega.tv/iframe.php?ref=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            url = common.parseDOM(result, "ul", attrs = { "class": "listing-videos.+?" })[0]
            url = common.parseDOM(url, "li", attrs = { "class": ".+?" })
            url = [i for i in url if any(x in resolver().cleantitle_movie(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div", attrs = { "class": "video-embed" })[0]
            url = re.compile("ref='(.+?)'").findall(url)[0]
            url = self.player_link % url
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().videomega(url)
            if url == None: return

            movieshd_sources.append({'source': 'MoviesHD', 'quality': 'HD', 'provider': 'MoviesHD', 'url': url})
        except:
            return

    def resolve(self, url):
        return url

class muchmovies:
    def __init__(self):
        global muchmovies_sources
        muchmovies_sources = []
        self.base_link = 'http://www.muchmovies.org'
        self.search_link = 'http://www.muchmovies.org/search'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link + '/' + urllib.quote_plus(title.replace(' ', '-'))

            result = getUrl(query, mobile=True).result
            url = common.parseDOM(result, "li", attrs = { "data-icon": "false" })
            url = [i for i in url if any(x in resolver().cleantitle_movie(i) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            muchmovies_sources.append({'source': 'Muchmovies', 'quality': 'HD', 'provider': 'Muchmovies', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url, mobile=True).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "data-role": "button" })
            url = [i for i in url if str('.mp4') in i][0]
            return url
        except:
            return

class glowgaze:
    def __init__(self):
        global glowgaze_sources
        glowgaze_sources = []
        self.base_link = 'http://g2g.fm'
        self.forum_link = 'http://g2g.fm/forum'
        self.search_link = 'http://g2g.fm/forum/search.php?do=process&titleonly=1&query=online+%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "div", attrs = { "class": "threadinfo thread" })
            url = [i for i in url if any(x in resolver().cleantitle_movie(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            name = common.parseDOM(url, "a", attrs = { "class": "title" })[0]
            url = common.parseDOM(url, "a", ret="href", attrs = { "class": "title" })[0]
            url = re.findall('(.+?[?]\d+)-', url, re.I)[0]
            url = '%s/%s' % (self.forum_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if ' Season ' in name and ' Episode ' in name: raise Exception()
            if ' 1080p ' in name or ' 720p ' in name: quality = 'HD'
            else: quality = 'SD'

            url = getUrl(url).result
            url = url.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(url, "iframe", ret="src", attrs = { "webkitallowfullscreen": ".+?" })[0]
            url = getUrl(url, referer=self.base_link).result
            url = common.parseDOM(url, "iframe", ret="src")[0]
            url = getUrl(url, referer=self.base_link).result

            u = re.compile('"(https://redirector.googlevideo.com/.+?)"').findall(url)
            u += re.compile('"(http://redirector.googlevideo.com/.+?)"').findall(url)
            u += re.compile('"(https://docs.google.com/.+?)"').findall(url)
            u += re.compile('"(http://docs.google.com/.+?)"').findall(url)
            url = u[-1]

            if 'docs.google.com' in url:
                import commonresolvers
                url = commonresolvers.resolvers().googledocs(url)
                if url == None: return
            elif 'googlevideo.com' in url:
                url = getUrl(url, output='geturl').result

            glowgaze_sources.append({'source': 'Glowgaze', 'quality': quality, 'provider': 'Glowgaze', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class movietube:
    def __init__(self):
        global movietube_sources
        movietube_sources = []
        self.base_link = 'http://www.movietube.cc'
        self.index_link = 'http://www.movietube.cc/index.php'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            post = urllib.urlencode({'a': 'retrieve', 'c': 'result', 'p': '{"KeyWord":"%s","Page":"1","NextToken":""}' % title})
            result = getUrl(self.index_link, post=post).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "tr")
            url = [i for i in url if any(x in resolver().cleantitle_movie(re.sub('[(]\d{4}[)]', '<', i)) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = url.split('?v=')[-1]

            post = urllib.urlencode({'a': 'getmoviealternative', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
            result = getUrl(self.index_link, post=post).result
            if not result == '':
                result = re.compile('(<a.+?</a>)').findall(result)
                result = [i for i in result if '0000000008400000' in i or '0000000008100000' in i]
                u = [i for i in result if '>1080p<' in i]
                u += [i for i in result if '>720p<' in i]
                u = [common.parseDOM(i, "a", ret="href")[0] for i in u]
                u = [i.split('?v=')[-1] for i in u]
                u = u[:3]
            else:
                u = [url]

            for i in u:
                try:
                    post = urllib.urlencode({'a': 'getplayerinfo', 'c': 'result', 'p': '{"KeyWord":"%s"}' % url})
                    result = getUrl(self.index_link, post=post).result

                    try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
                    except: url = common.parseDOM(result, "iframe", ret="src")[0]

                    if 'docs.google.com' in url:
                        import commonresolvers
                        url = commonresolvers.resolvers().googledocs(url)
                        if url == None: raise Exception()
                    elif 'googlevideo.com' in url:
                        url = getUrl(url, output='geturl').result

                    movietube_sources.append({'source': 'Movietube', 'quality': 'HD', 'provider': 'Movietube', 'url': url})
                    return
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class yify:
    def __init__(self):
        global yify_sources
        yify_sources = []
        self.base_link = 'http://yify.tv'
        self.ajax_link = 'http://yify.tv/wp-admin/admin-ajax.php'
        self.post_link = 'action=ajaxy_sf&sf_value=%s'
        self.player_link = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p2.php?url=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.post_link % (urllib.quote_plus(title))

            result = getUrl(self.ajax_link, post=query).result
            result = result.replace('&#8211;','-')
            url = json.loads(result)
            url = url['post']['all']
            url = [i['post_link'] for i in url if any(x == resolver().cleantitle_movie(i['post_title']) for x in [resolver().cleantitle_movie(title), resolver().cleantitle_movie(title)])][0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            if not str('tt' + imdb) in result: raise Exception()

            url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(result)[0]
            url = self.player_link % url

            result = getUrl(url, referer=url).result
            result = json.loads(result)

            url = [i['url'] for i in result if 'x-shockwave-flash' in i['type']]
            url += [i['url'] for i in result if 'video/mpeg4' in i['type']]
            url = url[-1]

            yify_sources.append({'source': 'YIFY', 'quality': 'HD', 'provider': 'YIFY', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class shush:
    def __init__(self):
        global shush_sources
        shush_sources = []
        self.base_link = 'http://www.shush.se'
        self.search_link = 'http://www.shush.se/index.php?shows'
        self.show_link = 'http://www.shush.se/index.php?showlist=%s'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            result = getUrl(self.search_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "shows" })

            url = [common.parseDOM(i, "a", ret="href")[0] for i in result]
            url = [i.split('showlist=')[-1] for i in url]
            url = [i for i in url if any(x == resolver().cleantitle_tv(i) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])][0]
            url = self.show_link % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "list" })
            result = [i for i in result if ' Season %01d Episode: %01d '% (int(season), int(episode)) in i][0]

            t = common.parseDOM(result, "a")[0]
            t = t.split(' Season %01d Episode: %01d '% (int(season), int(episode)))[-1].split(' ', 1)[-1]
            if not resolver().cleantitle_tv(title.encode('utf-8').lower()) == resolver().cleantitle_tv(t.encode('utf-8').lower()): return

            url = common.parseDOM(result, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import GKDecrypter
            result = getUrl(url).result
            url = re.compile('proxy[.]link=shush[*](.+?)&').findall(result)[-1]
            url = GKDecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('djRBdVhhalplRm83akFNZ1VOWkI='),'ECB').split('\0')[0]

            import commonresolvers
            if 'docs.google.com' in url:
                url = commonresolvers.resolvers().googledocs(url)
            elif 'picasaweb.google.com' in url:
                url = commonresolvers.resolvers().picasaweb(url)
            else:
                return

            if not any(x in url for x in ['&itag=22&', '&itag=37&', '&itag=38&', '&itag=45&', '&itag=84&', '&itag=102&', '&itag=120&', '&itag=121&']): return

            shush_sources.append({'source': 'Shush', 'quality': 'HD', 'provider': 'Shush', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            url = getUrl(url, output='geturl').result
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

class ororo:
    def __init__(self):
        global ororo_sources
        ororo_sources = []
        self.base_link = 'http://ororo.tv'
        self.key_link = base64.urlsafe_b64decode('dXNlciU1QnBhc3N3b3JkJTVEPWMyNjUxMzU2JnVzZXIlNUJlbWFpbCU1RD1jMjY1MTM1NiU0MGRyZHJiLmNvbQ==')
        self.sign_link = 'http://ororo.tv/users/sign_in'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            result = getUrl(self.base_link).result

            if not "'index show'" in result:
                result = getUrl(self.sign_link, post=self.key_link, close=False).result
                result = getUrl(self.base_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "index show" })

            match = [i for i in result if any(x == resolver().cleantitle_tv(common.parseDOM(i, "a", attrs = { "class": "name" })[0]) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])]
            match2 = [i for i in match if any(x in i for x in ['>%s<' % str(year), '>%s<' % str(int(year)+1), '>%s<' % str(int(year)-1)])][0]
            url = common.parseDOM(match2, "a", ret="href")[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "a", ret="data-href", attrs = { "href": "#%01d-%01d" % (int(season), int(episode)) })[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            ororo_sources.append({'source': 'Ororo', 'quality': 'SD', 'provider': 'Ororo', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url).result

            if not "my_video" in result:
                result = getUrl(self.sign_link, post=self.key_link, close=False).result
                result = getUrl(url).result

            url = None
            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/webm" })[0]
            except: pass
            try: url = url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: pass

            if url is None: return
            if not url.startswith('http://'): url = '%s%s' % (self.base_link, url)
            url = '%s|Cookie=%s' % (url, urllib.quote_plus('video=true'))

            return url
        except:
            return

class putlockertv:
    def __init__(self):
        global putlockertv_sources
        putlockertv_sources = []
        self.base_link = 'http://putlockertvshows.me'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            result = getUrl(self.base_link).result
            result = common.parseDOM(result, "tr", attrs = { "class": "fc" })

            match = [i for i in result if any(x == resolver().cleantitle_tv(common.parseDOM(i, "a")[0]) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])][0]
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s%s/ifr/s%02de%02d.html' % (self.base_link, url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "div", ret="onclick", attrs = { "class": "badsvideo" })
            if url == []:
                url = common.parseDOM(result, "iframe", ret="src")[-1]
                url = '%s%s' % (self.base_link, url)
                result = getUrl(url).result
                url = common.parseDOM(result, "div", ret="onclick", attrs = { "class": "badsvideo" })
            url = re.compile(".*'(.+?)'").findall(url[0])[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = url.replace('putlocker', 'firedrive')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if 'firedrive' in url: source = 'Firedrive'
            elif 'mail.ru' in url: source = 'Mailru'
            else: return

            putlockertv_sources.append({'source': source, 'quality': 'SD', 'provider': 'PutlockerTV', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class clickplay:
    def __init__(self):
        global clickplay_sources
        clickplay_sources = []
        self.base_link = 'http://clickplay.to'
        self.search_link = 'http://clickplay.to/search/%s'

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.search_link % urllib.quote_plus(' '.join([i for i in show.split() if i not in ['The','the','A','a']]))
            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "id": "video_list" })[0]
            result = result.split('</a>')

            match = [i for i in result if any(x in resolver().cleantitle_tv(i) for x in [str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(year) + '<'), str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(int(year)+1) + '<'), str('>' + resolver().cleantitle_tv(show) + '(%s)' % str(int(year)-1) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(year) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(int(year)+1) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '(%s)' % str(int(year)-1) + '<')])][0]
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%sseason-%01d/episode-%01d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import GKDecrypter
            result = getUrl(url).result
            links = re.compile('<a href="([?]link_id=.+?)".+?rel="noindex, nofollow".+?\[720p\].+?</a>').findall(result)
            u = re.compile('content="(%s.+?)"' % url).findall(result)[0]

            for i in links[:5]:
                try:
                    result = getUrl(u + i).result
                    url = re.compile('proxy[.]link=clickplay[*](.+?)"').findall(result)[-1]
                    url = GKDecrypter.decrypter(198,128).decrypt(url,base64.urlsafe_b64decode('bW5pcUpUcUJVOFozS1FVZWpTb00='),'ECB').split('\0')[0]
                    if 'vk.com' in url:
                        import commonresolvers
                        vk = commonresolvers.resolvers().vk(url)
                        for i in vk: clickplay_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Clickplay', 'url': i['url']})
                    elif 'firedrive' in url:
                        clickplay_sources.append({'source': 'Firedrive', 'quality': 'HD', 'provider': 'Clickplay', 'url': url})
                    elif 'mail.ru' in url:
                        clickplay_sources.append({'source': 'Mailru', 'quality': 'SD', 'provider': 'Clickplay', 'url': url})
                except:
                    pass
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class vkbox:
    def __init__(self):
        global vkbox_sources
        vkbox_sources = []
        self.base_link = 'http://mobapps.cc'
        self.data_link = 'http://mobapps.cc/data/data_en.zip'
        self.moviedata_link = 'movies_lite.json'
        self.tvdata_link = 'tv_lite.json'
        self.moviesearch_link = 'http://mobapps.cc/api/serials/get_movie_data/?id=%s'
        self.tvsearch_link = 'http://mobapps.cc/api/serials/e/?h=%s&u=%s&y=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            #result = self.getdata(self.moviedata_link)
            result = cache2(self.getdata, self.moviedata_link)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == resolver().cleantitle_movie(i['title']) for x in [resolver().cleantitle_movie(title), resolver().cleantitle_movie(title)]) and any(x == i['year'] for x in [str(year), str(int(year)+1), str(int(year)-1)])][0]
            url = self.moviesearch_link % match
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=10)
            result = response.read()
            response.close()

            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + 537
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: vkbox_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            #result = self.getdata(self.tvdata_link)
            result = cache2(self.getdata, self.tvdata_link)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == resolver().cleantitle_tv(i['title']) for x in [resolver().cleantitle_tv(show), resolver().cleantitle_tv(show_alt)])][0]
            url = self.tvsearch_link % (match, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=10)
            result = response.read()
            response.close()

            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + int(season) + int(episode)
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: vkbox_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'VKBox', 'url': i['url']})
        except:
            return

    def getdata(self, file):
        try:
            import zipfile, StringIO
            data = urllib2.urlopen(self.data_link, timeout=10).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            result = zip.read(file)
            zip.close()
            return result
        except:
            return

    def resolve(self, url):
        return url

class istreamhd:
    def __init__(self):
        global istreamhd_sources
        istreamhd_sources = []
        self.base_link = 'http://istreamhd.org'
        self.login_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2F1dGhlbnRpY2F0ZS5waHA='
        self.search_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL3NlYXJjaC5waHA='
        self.show_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF9zaG93LnBocA=='
        self.get_link = 'aHR0cDovL2lzdHJlYW1oZC5vcmcvYXBpL2dldF92aWRlby5waHA='
        self.mail, self.password = getSetting("istreamhd_mail"), getSetting("istreamhd_password")

    def mv(self, name, title, year, imdb, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            post = urllib.urlencode({'e-mail': self.mail, 'password': self.password})
            result = getUrl(base64.urlsafe_b64decode(self.login_link), post=post).result
            result = json.loads(result)
            token = result['auth']['token']

            post = urllib.urlencode({'token': token, 'query': title})
            result = getUrl(base64.urlsafe_b64decode(self.search_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if str('tt' + imdb) in i['imdb_id']][0]
            url = url['id']

            post = urllib.urlencode({'token': token, 'vid_id': url})
            result = getUrl(base64.urlsafe_b64decode(self.get_link), post=post).result
            result = json.loads(result)
            url = result['video']['url']
            url = url.replace('http://', 'https://')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: istreamhd_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'iStreamHD', 'url': i['url']})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            post = urllib.urlencode({'e-mail': self.mail, 'password': self.password})
            result = getUrl(base64.urlsafe_b64decode(self.login_link), post=post).result
            result = json.loads(result)
            token = result['auth']['token']

            post = urllib.urlencode({'token': token, 'query': show})
            result = getUrl(base64.urlsafe_b64decode(self.search_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if str('tt' + imdb) in i['poster']][0]

            post = urllib.urlencode({'token': token, 'show': url['title'], 'cat_id': url['cat_id']})
            result = getUrl(base64.urlsafe_b64decode(self.show_link), post=post).result
            result = json.loads(result)
            url = result['result']['items']
            url = [i for i in url if i['season'] == str('%01d' % int(season)) and  i['episode'] == str('%01d' % int(episode))][0]
            url = url['vid_id']

            post = urllib.urlencode({'token': token, 'vid_id': url})
            result = getUrl(base64.urlsafe_b64decode(self.get_link), post=post).result
            result = json.loads(result)
            url = result['video']['url']
            url = url.replace('http://', 'https://')
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: istreamhd_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'iStreamHD', 'url': i['url']})
        except:
            return

    def resolve(self, url):
        return url

class simplymovies:
    def __init__(self):
        global simplymovies_sources
        simplymovies_sources = []
        self.base_link = 'http://simplymovies.net'
        self.moviesearch_link = 'http://simplymovies.net/index.php?searchTerm='
        self.tvsearch_link = 'http://simplymovies.net/tv_shows.php?searchTerm='

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.moviesearch_link + urllib.quote_plus(title.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in resolver().cleantitle_movie(i) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [', %s<' % str(year), ', %s<' % str(int(year)+1), ', %s<' % str(int(year)-1)])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: simplymovies_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Simplymovies', 'url': i['url']})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.tvsearch_link + urllib.quote_plus(show.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in resolver().cleantitle_tv(i) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = result.split('<h3>')
            url = [i for i in url if str('Season %01d</h3>' % int(season)) in i][-1]
            url = url.replace(':','<')
            url = re.compile('.*href="(.+?)">Episode %01d<' % int(episode)).findall(url)[0]
            url = '%s/%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            import commonresolvers
            url = commonresolvers.resolvers().vk(url)
            for i in url: simplymovies_sources.append({'source': 'VK', 'quality': i['quality'], 'provider': 'Simplymovies', 'url': i['url']})
        except:
            return

    def resolve(self, url):
        return url

class moviestorm:
    def __init__(self):
        global moviestorm_sources
        moviestorm_sources = []
        self.base_link = 'http://moviestorm.eu'
        self.search_link = 'http://moviestorm.eu/search?q=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(title))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "links" })[0]
            links = common.parseDOM(result, "tr")
            links = [i for i in links if 'http://ishared.eu/' in i]

            sd_links = [re.compile('"(http://ishared.eu/.+?)"').findall(i)[0] for i in links if not any(x in common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0] for x in ['CAM', 'TS'])]
            ts_links = [re.compile('"(http://ishared.eu/.+?)"').findall(i)[0] for i in links if any(x in common.parseDOM(i, "td", attrs = { "class": "quality_td" })[0] for x in ['CAM', 'TS'])]

            if (len(sd_links) == 1):
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': sd_links[0]})
            if (len(ts_links) == 1):
                moviestorm_sources.append({'source': 'iShared', 'quality': 'CAM', 'provider': 'Moviestorm', 'url': ts_links[0]})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            query = self.search_link % (urllib.quote_plus(show))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s?season=%01d&episode=%01d' % (url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "id": "searialinks" })[0]
            links = re.compile('"(http://ishared.eu/.+?)"').findall(result)

            for url in links:
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            import commonresolvers
            url = commonresolvers.resolvers().get(url)
            return url
        except:
            return

class noobroom:
    def __init__(self):
        global noobroom_sources
        noobroom_sources = []
        self.base_link = 'http://superchillin.com'
        self.search_link = 'http://superchillin.com/search.php?q=%s'
        self.login_link = 'http://superchillin.com/login.php'
        self.login2_link = 'http://superchillin.com/login2.php'
        self.mail, self.password = getSetting("noobroom_mail"), getSetting("noobroom_password")

    def mv(self, name, title, year, imdb, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            query = self.search_link % (urllib.quote_plus(title))

            result = self.login()
            result = getUrl(query).result

            url = re.compile('(<i>Movies</i>.+)').findall(result)[0]
            url = url.split("'tippable'")
            url = [i for i in url if any(x in resolver().cleantitle_movie(i) for x in [str('>' + resolver().cleantitle_movie(title) + '<')]) and any(x in i for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])][0]
            url = re.compile("href='(.+?)'").findall(url)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result

            if not str('tt' + imdb) in result: raise Exception()

            links = re.compile('"file": "(.+?)"').findall(result)
            try: u = [i for i in links if 'type=flv' in i][0]
            except: pass
            try: u = [i for i in links if 'type=mp4' in i][0]
            except: pass
            url = '%s%s' % (self.base_link, u)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try:
                quality = 'SD'
                q = re.compile('"width": "(.+?)"').findall(result)[0]
                if int(q) > 720: quality = 'HD'
            except:
                pass

            noobroom_sources.append({'source': 'Noobroom', 'quality': quality, 'provider': 'Noobroom', 'url': url})
        except:
            return

    def tv(self, name, title, year, imdb, tvdb, season, episode, show, show_alt, hostDict):
        try:
            if (self.mail == '' or self.password == ''): raise Exception()

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if 'UK' in country and not 'USA' in country: return

            query = self.search_link % (urllib.quote_plus(show))

            result = self.login()
            result = getUrl(query).result

            url = re.compile('(<i>TV Series</i>.+)').findall(result)[0]
            url = url.split("><a ")
            url = [i for i in url if any(x in resolver().cleantitle_tv(i) for x in [str('>' + resolver().cleantitle_tv(show) + '<'), str('>' + resolver().cleantitle_tv(show_alt) + '<')])][0]
            url = re.compile("href='(.+?)'").findall(url)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile("<b>%01dx%02d .+?style=.+? href='(.+?)'" % (int(season), int(episode))).findall(result)[0]
            url = '%s%s' % (self.base_link, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            links = re.compile('"file": "(.+?)"').findall(result)
            try: u = [i for i in links if 'type=flv' in i][0]
            except: pass
            try: u = [i for i in links if 'type=mp4' in i][0]
            except: pass
            url = '%s%s' % (self.base_link, u)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            try:
                quality = 'SD'
                q = re.compile('"width": "(.+?)"').findall(result)[0]
                if int(q) > 720: quality = 'HD'
            except:
                pass

            noobroom_sources.append({'source': 'Noobroom', 'quality': quality, 'provider': 'Noobroom', 'url': url})
        except:
            return

    def login(self):
        try:
            post = urllib.urlencode({'email': self.mail, 'password': self.password})
            result = getUrl(self.login_link, close=False).result
            cookie = getUrl(self.login_link, output='cookie').result
            result = urllib2.Request(self.login2_link, post)
            result = urllib2.urlopen(result, timeout=10)
        except:
            return

    def resolve(self, url):
        try:
            result = self.login()
            try: u = getUrl(url, output='geturl').result
            except: pass
            try: u = getUrl(url.replace('&hd=0', '&hd=1'), output='geturl').result
            except: pass
            return u
        except:
            return

class einthusan:
    def __init__(self):
        global einthusan_sources
        einthusan_sources = []
        self.base_link = 'http://www.einthusan.com'
        self.search_link = 'http://www.einthusan.com/search/?search_query=%s&lang=%s'

    def mv(self, name, title, year, imdb, hostDict):
        try:
            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = [i.strip() for i in search['Country'].split(',')]
            if not 'India' in country: return

            language = [i.strip().lower() for i in search['Language'].split(',')]
            language = [i for i in language if any(x == i for x in ['hindi', 'tamil', 'telugu', 'malayalam'])][0]

            query = self.search_link % (urllib.quote_plus(title), language)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "search-category" })
            result = [i for i in result if 'Movies' in common.parseDOM(i, "p")[0]][0]
            result = common.parseDOM(result, "li")

            url = [i for i in result if any(x in resolver().cleantitle_movie(common.parseDOM(i, "a")[0]) for x in [resolver().cleantitle_movie(title)]) and any(x in common.parseDOM(i, "a")[0] for x in [' (%s)' % str(year), ' (%s)' % str(int(year)+1), ' (%s)' % str(int(year)-1)])]
            if len(url) == 0:
                url = [i for i in result if any(x == resolver().cleantitle_movie(common.parseDOM(i, "a")[0]) for x in [resolver().cleantitle_movie(title)])]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = url.replace('../', '%s/' % self.base_link)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result

            y = common.parseDOM(result, "div", attrs = { "class": "movie-description" })[0]
            if not any(x in y for x in [str(year), str(int(year)+1), str(int(year)-1)]): return

            url = re.compile("'file': '(.+?)'").findall(result)[0]

            einthusan_sources.append({'source': 'Einthusan', 'quality': 'HD', 'provider': 'Einthusan', 'url': url})
        except:
            return

    def resolve(self, url):
        return url


main()