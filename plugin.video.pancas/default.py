# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib, urllib2, re, os, sys, math, unicodedata
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.video.pancas')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos/'))
playlists = xbmc.translatePath(os.path.join(home, 'resources', 'playlists/'))
localm3u = mysettings.getSetting('local_m3u')
onlinem3u = mysettings.getSetting('online_m3u')
localxml = mysettings.getSetting('local_xml')
onlinexml = mysettings.getSetting('online_xml')
localizedString = mysettings.getLocalizedString
m3u_regex = '#.+?,(.+)\s*(.+)\s*'
xml_channel_name = '<channel>\s*<name>(.+?)</name>\s*<thumbnail>(.*?)</thumbnail>'
xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
xml_regex_reg_1S = '<title>(.*?)</title>(?s).*?<page>(.*?)</page>(?s).*?<thumbnail>(.*?)</thumbnail>'
xml_regex_reg_2L = '<title>(.*?)</title>\s*<link>.*?</link>\s*<regex>\s*<name>.*?</name>\s*<expres>.*?</expres>\s*<page>(.*?)</page>\s*<referer>.*?</referer>\s*</regex>\s*<thumbnail>(.*?)</thumbnail>'
my_dict = {'&#7893;':'ổ', '&#7907;':'ợ', '&#7885;':'ọ', '&#7909;':'ụ', '&#7875;':'ể', '&#7843;':'ả', '&#7871;':'ế', '&#7897;':'ộ', '&#7889;':'ố', '&#7873;':'ề', '&#7883;':'ị', '&#7855;':'ắ'}
tvreplay = 'http://113.160.49.39/tvcatchup/'
u_tube = 'http://www.youtube.com'
tvviet = 'http://tv.vnn.vn/'

tv_mode = mysettings.getSetting('tv_mode')
if len(tv_mode) <= 0:
	xbmcgui.Dialog().ok(localizedString(10001), localizedString(10002), localizedString(10003), localizedString(10004))
	mysettings.openSettings()

def get_cookie():
	from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
	import cookielib
	cj = cookielib.CookieJar()
	opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
	req = Request(tvviet)
	f = opener.open(req)
	for cookie in cj:
		return "%s=%s" % (cookie.name, cookie.value)      

def replace_all(text, my_dict):
	try:
		for a, b in my_dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass	

def read_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content	
	except:
		pass 

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		req.add_header('Cookie', get_cookie())
		response = urllib2.urlopen(req, timeout = 60)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
			
def convertSize(size):
   size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size, 1024)))
   p = math.pow(1024, i)
   s = round(size/p, 2)
   if (s > 0):
       return '%s %s' % (s, size_name[i])
   else:
       return '0B'

def main():
	add_dir('[B][COLOR lime]-[COLOR orange]-[COLOR cyan]>[COLOR magenta]> [COLOR yellow]Channel SUPER Search [COLOR red] * [COLOR white]BE PATIENT[COLOR red] * [COLOR lime] [COLOR magenta]<[COLOR cyan]<[COLOR orange]-[COLOR lime]-[/COLOR][/B]', 'searchlink', 91, logos + 'menu_search.png', fanart) 
	content = read_file(playlists + 'MainMenu.xml')
	match = re.compile(xml_regex + '\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, add_dir_mode in match:
		add_dir(name, url, add_dir_mode, logos + thumb, fanart) 

def direct_link():
	add_dir('[COLOR lime]-[COLOR cyan]-[COLOR orange]>[COLOR magenta]> [COLOR lime][B]Channel Search[COLOR magenta] * [COLOR white][/B] [COLOR magenta]<[COLOR orange]<[COLOR cyan]-[COLOR lime]-[/COLOR]', 'searchlink', 90, logos + 'direct_search.png', fanart) 
	content = read_file(playlists + 'direct_link.m3u')
	match = re.compile(m3u_regex).findall(content)
	for name, url in match:
		direct_link_action(name, url)
		
def search_main(): 
	try:
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')						
		try:
			link = read_file(playlists + 'my_tv.xml')	
			match = re.compile(xml_channel_name).findall(link)
			for channel_name, thumb in match:
				if re.search(searchText, removeAccents(channel_name.replace('Đ', 'D')), re.IGNORECASE):					
					if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
						add_link(channel_name, u_tube, 201, logos + 'mytv.png', fanart)
					else:
						add_dir(channel_name, 'xmlfile', 301, logos + 'mytv.png', fanart)						
			match = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(link)	
			for vlink in match:
				final_link = re.compile(xml_regex).findall(vlink)
				for title, url, thumb in final_link:
					if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
						if len(thumb) <= 0:
							add_link(title, url, 201, logos + 'mytv.png', fanart)
						else:
							add_link(title, url, 201, thumb, fanart)
		except:
			pass
		try:
			link = read_file(playlists + 'thanh51.xml')
			match = re.compile(xml_channel_name).findall(link)
			for channel_name, thumb in match:
				if re.search(searchText, removeAccents(channel_name.replace('Đ', 'D')), re.IGNORECASE):					
					if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
						add_link(channel_name, u_tube, 201, logos + 'thanh51.png', fanart)
					else:
						add_dir(channel_name, 'xmlfile', 302, logos + 'thanh51.png', fanart)
			match = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(link)	
			for vlink in match:
				if '<page>' in vlink:
					final_link = re.compile(xml_regex_reg_2L).findall(vlink)
					for title, url, thumb in final_link:
						if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
							if len(thumb) <= 0:
								add_link(title.strip(), url, 202, logos + 'thanh51.png', fanart)		
							else:
								add_link(title.strip(), url, 202, thumb, fanart) 
				else:		
					final_link = re.compile(xml_regex).findall(vlink)
					for title, url, thumb in final_link:
						if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
							if len(thumb) <= 0:
								add_link(title.strip(), url, 201, logos + 'thanh51.png', fanart) 
							else:	
								add_link(title.strip(), url, 201, thumb, fanart)					
		except:
			pass
		try:
			content = read_file(playlists + 'thanh51.m3u')
			if '<CHANNEL>' in content:
				match = re.compile('<NAME>(.+?)</NAME>').findall(content)
				for channel_name in match:
					if re.search(searchText, removeAccents(channel_name.replace('Đ', 'D')), re.IGNORECASE):			
						if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
							add_link(channel_name.strip(), u_tube, 201, logos + 'thanh51.png', fanart)
						else:	
							add_dir(channel_name.strip(), url, 303, logos + 'thanh51.png', fanart)  
			else:
				match = re.compile(m3u_regex).findall(content)
				for title, url in match:
					if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):			
						if 'UPDATED ON' in title or 'CẬP NHẬT' in title:
							add_link(title.strip(), u_tube, 201, logos + 'thanh51.png', fanart)
						else:
							add_link(title.strip(), url, 201, logos + 'thanh51.png', fanart)								
		except:
			pass		
		try:
			content = read_file(playlists + 'ATF01.m3u')	
			match = re.compile(m3u_regex).findall(content)
			for title, url in match:
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					if 'UPDATED ON' in title or 'CẬP NHẬT' in title:
						add_link(title.strip(), u_tube, 201, logos + 'atf01.png', fanart)
					else:
						add_link(title.strip(), url, 201, logos + 'atf01.png', fanart)		
		except:
			pass
		try:
			content = read_file(playlists + 'uTube.xml')
			match = re.compile(xml_regex).findall(content)
			for title, url, thumb in match:
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):			
					if 'OverseaNews' in title:
						if len(thumb) > 0:
							if thumb.startswith ('http'):
								add_dir(title.replace('OverseaNews - ', ''), url, '', thumb, fanart)
							else:
								add_dir(title.replace('OverseaNews - ', ''), url, '', logos + 'haingoaitube.png', fanart)						
						else:
							add_dir(title.replace('OverseaNews - ', ''), url, '', logos + 'haingoaitube.png', fanart)
					elif 'Religion' in title:
						if len(thumb) < 1:				
							add_dir(title.replace('Religion - ', ''), url, '', logos + 'religiontube.png', fanart)	
						else:
							if thumb.startswith ('http'):				
								add_dir(title.replace('Religion - ', ''), url, '', thumb, fanart)
							else:
								add_dir(title.replace('Religion - ', ''), url, '', logos + 'religiontube.png', fanart)	

					elif 'NewsInVN' in title:
						if '(DailyMotion)' in title:
							pass
						else:
							if len(thumb) > 0:
								if thumb.startswith ('http'):					
									add_dir(title.replace('NewsInVN - ', ''), url, '', thumb, fanart)
								else:
									add_dir(title.replace('NewsInVN - ', ''), url, '', logos + 'vntube.png', fanart)							
							else:
								add_dir(title.replace('NewsInVN - ', ''), url, '', logos + 'vntube.png', fanart)		
		except:
			pass		
		try:
			content = make_request(tvreplay)
			match = re.compile('href="(\d+)/">(\d+)/<').findall(content)
			for url, name in match:
				content = make_request(tvreplay + url)
				match = re.compile('href="(.+?)">(.+?)\.mp4</a>(.+?)\n').findall(content)
				for href, title, VidSize in match:
					if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):			
						title = title.split('_')[0] + '_' + title.split('_')[-1]
						video_size = convertSize(int(VidSize.split(' ')[-1]))
						add_link(title + ' [COLOR magenta]* [COLOR yellow]' + video_size + '[/COLOR]', url + '/' + href, 201, logos + 'tvreplay.png', fanart)
		except:
			pass
		try:
			content = make_request('http://www.htvonline.com.vn/livetv')
			match = re.compile('href="http://www.htvonline.com.vn/livetv/(.+?)-3(.+?)"(?:\s*)><img alt="" width=".+?" height=".+?" src="(.+?)">').findall(content)
			for name, url, thumb in match:
				if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
					url = 'http://www.htvonline.com.vn/livetv/' + name + '-3' + url
					name = name.replace('-', ' ').upper()			
					add_link(name, url, 202, thumb, thumb)	
		except:
			pass		
		try:
			content = make_request(tvviet)
			match = re.compile('href="\/(.+?)">\s*<img src="\/(.+?)".+?\/>\s*(.+?)\n').findall(content)
			for url, thumb, title in match:
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					title = replace_all(title, my_dict)	
					add_link(title, tvviet + url, 202, (tvviet + thumb).replace(' ', '%20'), fanart)  
		except:
			pass		
		try:
			if len(onlinexml) > 0:														
				link = make_request(onlinexml)
				if '<channel>' in link:
					match = re.compile(xml_channel_name).findall(link)
					for channel_name, thumb in match:
						if re.search(searchText, removeAccents(channel_name.replace('Đ', 'D')), re.IGNORECASE):					
							if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
								add_link(channel_name, u_tube, 201, logos + 'myxml.png', fanart)
							else:
								add_dir(channel_name, 'xmlfile', 33, logos + 'myxml.png', fanart)
					match = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(link)	
					for vlink in match:
						final_link = re.compile(xml_regex).findall(vlink)
						for title, url, thumb in final_link:
							if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
								if len(thumb) <= 0:
									add_link(title, url, 201, logos + 'myxml.png', fanart)
								else:
									add_link(title, url, 201, thumb, fanart)							
				else:
					match = re.compile(xml_regex).findall(link)
					for title, url, thumb in match:
						if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):				
							if len(thumb) > 0:
								add_link(title, url, 201, thumb, fanart) 
							else:	
								add_link(title, url, 201, logos + 'myxml.png', fanart) 
		except:
			pass
		try:
			if len(localxml) > 0:														
				myxml = open(localxml, 'r')  
				link = myxml.read()
				myxml.close()
				if '<channel>' in link:
					match = re.compile(xml_channel_name).findall(link)
					for channel_name, thumb in match:
						if re.search(searchText, removeAccents(channel_name.replace('Đ', 'D')), re.IGNORECASE):					
							if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
								add_link(channel_name, u_tube, 201, logos + 'myxml.png', fanart)
							else:
								add_dir(channel_name, 'xmlfile', 33, logos + 'myxml.png', fanart)
					match = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(link)	
					for vlink in match:
						final_link = re.compile(xml_regex).findall(vlink)
						for title, url, thumb in final_link:
							if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
								if len(thumb) <= 0:
									add_link(title, url, 201, logos + 'myxml.png', fanart)
								else:
									add_link(title, url, 201, thumb, fanart)							
				else:
					match = re.compile(xml_regex).findall(link)
					for title, url, thumb in match:
						if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):				
							if len(thumb) > 0:
								add_link(title, url, 201, thumb, fanart) 
							else:	
								add_link(title, url, 201, logos + 'myxml.png', fanart) 
		except:
			pass
		try:
			if len(onlinem3u) > 0: 
				content = make_request(onlinem3u)
				match = re.compile(m3u_regex).findall(content)
				for title, url in match:
					if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):			
						add_link(title, url, 201, logos + 'mym3u.png', fanart)
		except:
			pass
		try:
			if len(localm3u) > 0: 
				mym3u = open(localm3u, 'r')  
				link = mym3u.read()
				mym3u.close()
				match = re.compile(m3u_regex).findall(link)
				for title, url in match:
					if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):			
						add_link(title, url, 201, logos + 'mym3u.png', fanart)
		except:
			pass
	except:
		pass			

def search_my_tv_channel(name):	
	link = read_file(playlists + 'my_tv.xml')	
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(link)	
	for vlink in match:
		final_link = re.compile(xml_regex).findall(vlink)
		for title, url, thumb in final_link:
			if len(thumb) <= 0:
				add_link(title, url, 201, logos + 'mytv.png', fanart)
			else:
				add_link(title, url, 201, thumb, fanart)	

def search_thanh51_xml_channel(name):
	name = name.replace('[', '\[').replace(']', '\]').replace ('(', '\(').replace(')', '\)')	
	link = read_file(playlists + 'thanh51.xml')	
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(link)	
	for vlink in match:
		if '<page>' in vlink:
			final_link = re.compile(xml_regex_reg_2L).findall(vlink)
			for title, url, thumb in final_link:
				if len(thumb) <= 0:
					add_link(title.strip(), url, 202, logos + 'thanh51.png', fanart)		
				else:
					add_link(title.strip(), url, 202, thumb, fanart) 
		else:		
			final_link = re.compile(xml_regex).findall(vlink)
			for title, url, thumb in final_link:
				if len(thumb) <= 0:
					add_link(title.strip(), url, 201, logos + 'thanh51.png', fanart) 
				else:	
					add_link(title.strip(), url, 201, thumb, fanart) 					

def search_thanh51_m3u_channel(name):
	name = name.replace('[', '\[').replace(']', '\]').replace ('(', '\(').replace(')', '\)')	
	content = read_file(playlists + 'thanh51.m3u')	
	match = re.compile('#<CHANNEL>\s*#<NAME>' + name + '</NAME>((?s).*?)#</CHANNEL>').findall(content)
	vlink = re.compile(m3u_regex).findall(match[0])
	for title, ahref in vlink:	
		add_link(title.strip(), ahref, 201, logos + 'thanh51.png', fanart) 
		
def search_direct(): 	
	try:	
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')			
		content = read_file(playlists + 'direct_link.m3u')
		match = re.compile(m3u_regex).findall(content)
		for name, url in match:	
			if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):		
				direct_link_action(name, url)					
	except:
		pass
		
def direct_link_action(name, url):
	if 'htvonline' in url or 'giniko' in url or 'tv.vnn.vn' in url:
		add_link(name.strip(), url, 202, logos + 'directlink.png', fanart)
	else:	
		add_link(name.strip(), url, 201, logos + 'directlink.png', fanart)
		
def tv_directory(): 
	content = read_file(playlists + 'my_tv.xml')
	match = re.compile(xml_channel_name).findall(content)
	for channel_name, thumb in match:
		if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
			add_link(channel_name, u_tube, 201, icon, fanart)
		else:
			add_dir(channel_name, url, 2, logos + thumb, fanart) 

def tv_index(name):	
	name = name.replace('[', '\[').replace(']', '\]').replace ('(', '\(').replace(')', '\)')
	content = read_file(playlists + 'my_tv.xml')
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(content)
	for vlink in match:
		final_link = re.compile(xml_regex).findall(vlink)
		for title, url, thumb in final_link:
			if 'www.giniko.com' in url:
				add_link(title, url, 202, thumb, fanart)
			else:
				if len(thumb) <= 0:
					add_link(title, url, 201, iconimage, fanart) 
				else:	
					add_link(title, url, 201, thumb, fanart)  

def utube_channels(url):
	content = read_file(playlists + 'uTube.xml')
	match = re.compile(xml_regex).findall(content)
	for title, url, thumb in match:
		if 'dailymotion' in url:
			pass
		else:	
			if 'TV Hải Ngoại' in name: 
				if 'OverseaNews' in title:			
					if len(thumb) > 0:
						if thumb.startswith ('http'):
							add_dir(title.replace('OverseaNews - ', ''), url, '', thumb, fanart)
						else:
							add_dir(title.replace('OverseaNews - ', ''), url, '', logos + 'haingoaitube.png', fanart)						
					else:
						add_dir(title.replace('OverseaNews - ', ''), url, '', logos + 'haingoaitube.png', fanart)
			elif 'Tôn Giáo' in name: 
				if 'Religion' in title:
					if len(thumb) < 1:				
						add_dir(title.replace('Religion - ', ''), url, '', logos + 'religiontube.png', fanart)	
					else:
						if thumb.startswith ('http'):				
							add_dir(title.replace('Religion - ', ''), url, '', thumb, fanart)
						else:
							add_dir(title.replace('Religion - ', ''), url, '', logos + 'religiontube.png', fanart)	
			else:
				if 'NewsInVN' in title:
					if len(thumb) > 0:
						if thumb.startswith ('http'):					
							add_dir(title.replace('NewsInVN - ', ''), url, '', thumb, fanart)
						else:
							add_dir(title.replace('NewsInVN - ', ''), url, '', logos + 'vntube.png', fanart)							
					else:
						add_dir(title.replace('NewsInVN - ', ''), url, '', logos + 'vntube.png', fanart)		

def tv_scraper(url):
	content = make_request(url)
	if 'htvonline' in url:
		match = re.compile('href="http://www.htvonline.com.vn/livetv/(.+?)-3(.+?)"(?:\s*)><img alt="" width=".+?" height=".+?" src="(.+?)">').findall(content)
		for name, url, thumb in match:
			url = 'http://www.htvonline.com.vn/livetv/' + name + '-3' + url
			name = name.replace('-', ' ').upper()			
			add_link(name, url, 202, thumb, thumb)			
	elif 'tv.vnn.vn' in url:
		match = re.compile('href="\/(.+?)">\s*<img src="\/(.+?)".+?\/>\s*(.+?)\n').findall(content)
		for url, thumb, title in match:
			title = replace_all(title, my_dict)	
			add_link(title, tvviet + url, 202, (tvviet + thumb).replace(' ', '%20'), fanart)  	  
	elif 'tvcatchup' in url:
		match = re.compile('href="(\d+)/">(\d+)/<').findall(content)
		for url, name in match:
			add_dir(name, tvreplay + url, 121, iconimage, fanart)			
	   
def tvreplay_link(url):
	content = make_request(url)
	match = re.compile('href="(.+?)">(.+?)\.mp4</a>(.+?)\n').findall(content)
	for href, name, VidSize in match:
		name = name.split('_')[0] + '_' + name.split('_')[-1]
		video_size = convertSize(int(VidSize.split(' ')[-1]))
		add_link(name + ' [COLOR magenta]* [COLOR yellow]' + video_size + '[/COLOR]', url + '/' + href, 201, iconimage, fanart)

def my_playlist_directory():
	if 'XML' in name:
		add_dir('[COLOR cyan]Online XML Playlist Của Tui[/COLOR]', 'onlinexml', 32, iconimage, fanart)
		add_dir('[COLOR orange]Local XML Playlist Của Tui[/COLOR]', 'localxml', 32, iconimage, fanart)  
	else:
		add_dir('[COLOR yellow]My Online M3U Playlist[/COLOR]', 'onlinem3u', 32, iconimage, fanart)
		add_dir('[COLOR lime]My Local M3U Playlist[/COLOR]', 'localm3u', 32, iconimage, fanart)

def my_playlist_link():
	if 'Local M3U' in name:
		if len(localm3u) <= 0:
			mysettings.openSettings()
		else:  
			try:
				mym3u = open(localm3u, 'r')  
				link = mym3u.read()
				mym3u.close()
				match = re.compile(m3u_regex).findall(link)
				for title, url in match:
					add_link(title, url, 201, iconimage, fanart)
			except:
				pass 
	elif 'Online M3U' in name:
		if len(onlinem3u) > 0: 
			content = make_request(onlinem3u)
			match = re.compile(m3u_regex).findall(content)
			for title, url in match:
				add_link(title, url, 201, iconimage, fanart)
		else:		
			mysettings.openSettings()			
	elif 'Local XML' in name:
		if len(localxml) <= 0:
			mysettings.openSettings() 
		else:	  
			myxml = open(localxml, 'r')  
			link = myxml.read()
			myxml.close()
			if '<channel>' in link:
				match = re.compile(xml_channel_name).findall(link)
				for channel_name, thumb in match:
					if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
						add_link(channel_name, u_tube, 201, iconimage, fanart)
					else:
						add_dir(channel_name, 'xmlfile', 33, iconimage, fanart)
			else:
				match = re.compile(xml_regex).findall(link)
				for title, url, thumb in match:
					if len(thumb) > 0:
						add_link(title, url, 201, thumb, fanart) 
					else:	
						add_link(title, url, 201, iconimage, fanart)  
	elif 'Online XML' in name:
		if len(onlinexml) > 0: 
			link = make_request(onlinexml)
			if '<channel>' in link:
				match = re.compile(xml_channel_name).findall(link)
				for channel_name, thumb in match:
					if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
						add_link(channel_name, u_tube, 201, iconimage, fanart)
					else:		
						add_dir(channel_name, onlinexml, 33, iconimage, fanart)
			else:
				match = re.compile(xml_regex).findall(link)
				for title, url, thumb in match:
					if len(thumb) > 0:
						add_link(title, url, 201, thumb, fanart) 
					else:	
						add_link(title, url, 201, iconimage, fanart)  		  
		else:		  
			mysettings.openSettings()	

def my_playlist_channel(name, url):
	name = name.replace('[', '\[').replace(']', '\]').replace ('(', '\(').replace(')', '\)')
	if url == onlinexml:
		link = make_request(onlinexml)
	else:
		myxml = open(localxml, 'r')  
		link = myxml.read()
		myxml.close()
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(link)	
	for vlink in match:
		final_link = re.compile(xml_regex).findall(vlink)
		for title, url, thumb in final_link:
			if len(thumb) <= 0:
				add_link(title, url, 201, iconimage, fanart)
			else:
				add_link(title, url, 201, thumb, fanart)	
				
def thanh51_xml_m3u_directory():
	add_dir("[COLOR lime]thanh51's XML playlist[/COLOR]", playlists + 'thanh51.xml', 12, iconimage, fanart)  
	add_dir("[COLOR blue]thanh51's M3U playlist[/COLOR]", playlists + 'thanh51.m3u', 12, iconimage, fanart)  

def thanh51_xml_m3u_channel(url):	
	content = read_file(url)
	if 'thanh51.xml' in url:
		if '<channel>' in content:
			match = re.compile(xml_channel_name).findall(content)
			for channel_name, thumb in match:
				if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
					add_link(channel_name.strip(), u_tube, 201, iconimage, fanart)
				else:
					add_dir(channel_name.strip(), url, 13, iconimage, fanart)  	
		else:
			match = re.compile(xml_regex).findall(content)
			for title, url, thumb in match:
				if len(thumb) > 0:
					add_link(title.strip(), url, 201, thumb, fanart) 
				else:	
					add_link(title.strip(), url, 201, iconimage, fanart) 
	else:  
		if '<CHANNEL>' in content:
			match = re.compile('<NAME>(.+?)</NAME>').findall(content)
			for channel_name in match:
				if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
					add_link(channel_name.strip(), u_tube, 201, iconimage, fanart)
				else:	
					add_dir(channel_name.strip(), url, 13, iconimage, fanart)  
		else:
			match = re.compile(m3u_regex).findall(content)
			for name, url in match: 
				if 'UPDATED ON' in name or 'CẬP NHẬT' in name:
					add_link(name.strip(), u_tube, 201, iconimage, fanart)
				else:
					add_link(name.strip(), url, 201, iconimage, fanart)

def thanh51_xml_m3u_index(name, url):
	name = name.replace('[', '\[').replace(']', '\]').replace ('(', '\(').replace(')', '\)')
	content = read_file(url)
	if 'thanh51.xml' in url:  
		match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(content)	
		for vlink in match:
			if '<page>' in vlink:
				#final_link = re.compile(xml_regex_reg_1S).findall(vlink)
				final_link = re.compile(xml_regex_reg_2L).findall(vlink)
				for name, url, thumb in final_link:
					if len(thumb) <= 0:
						add_link(name.strip(), url, 202, iconimage, fanart)		
					else:
						add_link(name.strip(), url, 202, thumb, fanart) 
			else:		
				final_link = re.compile(xml_regex).findall(vlink)
				for title, url, thumb in final_link:
					if len(thumb) <= 0:
						add_link(title.strip(), url, 201, iconimage, fanart) 
					else:	
						add_link(title.strip(), url, 201, thumb, fanart)  
	else: 
		match = re.compile('#<CHANNEL>\s*#<NAME>' + name + '</NAME>((?s).*?)#</CHANNEL>').findall(content)
		vlink = re.compile(m3u_regex).findall(match[0])
		for title, ahref in vlink:	
			add_link(title.strip(), ahref, 201, iconimage, fanart) 

def atf01_m3u():
	content = read_file(playlists + 'ATF01.m3u')
	match = re.compile(m3u_regex).findall(content)
	for title, url in match:
		if 'UPDATED ON' in title or 'CẬP NHẬT' in title:
			add_link(title.strip(), u_tube, 201, iconimage, fanart)
		else:
			add_link(title.strip(), url, 201, iconimage, fanart)		
			
def play_my_playlist(url):
	media_url = url.replace('&amp;', '&')
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def resolve_url(url):	
	content = make_request(url)
	if 'htvonline' in url:   
		media_url = re.compile('data-source="(.+?)"').findall(content)[0] 
	elif 'giniko' in url: 
		media_url = re.compile('file: "(.+?)"').findall(content)[0]
	else:
		media_url = re.compile("file: '(.+?)'").findall(content)[0]  
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok	
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true')  
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  

params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url) < 1:
	if 'Menu Selection Mode' in tv_mode:
		main()
	else:
		direct_link()  	

elif mode == 1:
	tv_directory()

elif mode == 2:  
	tv_index(name)

elif mode == 3:
	tv_scraper(url)  

elif mode == 11:  
	thanh51_xml_m3u_directory()

elif mode == 12:
	thanh51_xml_m3u_channel(url)

elif mode == 13:
	thanh51_xml_m3u_index(name, url)

elif mode == 21:  
	atf01_m3u()  

elif mode == 31:
	my_playlist_directory()

elif mode == 32:
	my_playlist_link()  

elif mode == 33:  
	my_playlist_channel(name, url) 

elif mode == 40:	
	utube_channels(url)

elif mode == 90:	
	search_direct()

elif mode == 91:	
	search_main()
	
elif mode == 121: 
	tvreplay_link(url)  		

elif mode == 201:  
	play_my_playlist(url)

elif mode == 202:
	resolve_url(url)  

elif mode == 301:
	search_my_tv_channel(name)

elif mode == 302:
	search_thanh51_xml_channel(name)

elif mode == 302:
	search_thanh51_m3u_channel(name)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))