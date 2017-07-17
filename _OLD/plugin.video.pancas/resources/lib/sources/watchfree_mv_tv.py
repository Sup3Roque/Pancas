# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

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

# TODO: get Hosts Dict from urlresolver


import re,urllib,urlparse,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control

from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://www.watchfree.to'
        self.moviesearch_link = '/?keyword=%s&search_section=1'
        self.tvsearch_link = '/?keyword=%s&search_section=2'


    def get_movie(self, imdb, title, year):
        try:
            query = self.moviesearch_link % urllib.quote_plus(cleantitle.query(title))
            query = urlparse.urljoin(self.base_link, query)

            result = str(client.request(query)).decode('iso-8859-1').encode('utf-8')
            if 'page=2' in result: result += str(client.request(query + '&page=2')).decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(result, 'div', attrs = {'class': 'item'})

            title = 'watch' + cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]
            try: result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]
            except: pass

            match = [i[0] for i in result if title == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in match]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]

            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    result = client.request(urlparse.urljoin(self.base_link, i))
                    if imdb in str(result): url = i ; break
                except:
                    pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.tvsearch_link % urllib.quote_plus(cleantitle.query(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)

            result = str(client.request(query)).decode('iso-8859-1').encode('utf-8')
            if 'page=2' in result: result += str(client.request(query + '&page=2')).decode('iso-8859-1').encode('utf-8')

            result = client.parseDOM(result, 'div', attrs = {'class': 'item'})

            tvshowtitle = 'watch' + cleantitle.get(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            try: result = [(urlparse.urlparse(i[0]).path, i[1]) for i in result]
            except: pass

            match = [i[0] for i in result if tvshowtitle == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    result = client.request(urlparse.urljoin(self.base_link, i))
                    if imdb in str(result): url = i ; break
                except:
                    pass

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = url.replace('/watch-', '/tv-')
            url += '/season-%01d-episode-%01d' % (int(season), int(episode))
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        control.log('### WATCHFREE %s' %url)
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
            #control.log('### %s' % url)

            links = client.parseDOM(result, 'table', attrs = {'class': 'link_ite.+?'})
            for i in links:
                #control.log('### i %s' % i)

                try:
                    url = client.parseDOM(i, 'a', ret='href')
                    url = [x for x in url if 'gtfo' in x][-1]
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['gtfo'][0]
                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    #if not host in hostDict:
                    #    control.log('watchfree HOST; %s' % host)
                    #    raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    try: host = host.split('.')[0]
                    except: pass
                    quality = client.parseDOM(i, 'div', attrs = {'class': 'quality'})
                    if any(x in ['[CAM]', '[TS]'] for x in quality): quality = 'CAM'
                    else:  quality = 'SD'
                    #quality = quality.encode('utf-8')
                    sources.append({'source': host, 'quality': quality, 'provider': 'Watchfree', 'url': url})


                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return

