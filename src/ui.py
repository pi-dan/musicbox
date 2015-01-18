#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: omi
# @Date:   2014-08-24 21:51:57
# @Last Modified by:   pi-dan
# @Last Modified time: 2015-01-18 18:02:01


'''
网易云音乐 Ui
'''

import curses
from api import NetEase
from math import ceil
import subprocess

class Ui:
    def __init__(self):
        curses.setupterm()  #初始化终端
        self.screen = curses.initscr()
        self.LINES=curses.tigetnum('lines') #终端行数
        self.COLS=curses.tigetnum('cols')  #列数
        self.show_begin_line=int((int(self.LINES)-22)/2-1)
        # charactor break buffer
        curses.cbreak()
        self.screen.keypad(1)
        self.netease = NetEase()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)              
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)        



    def build_playinfo(self, song_name, artist, album_name, pause=False):
        curses.noecho()
        # refresh top 2 line
        self.screen.move(1+self.show_begin_line,1)
        self.screen.clrtoeol()
        self.screen.move(2+self.show_begin_line,1)
        self.screen.clrtoeol()
        if pause:
            self.screen.addstr(1+self.show_begin_line, 6, '_ _ z Z Z', curses.color_pair(3))
        else:
            self.screen.addstr(1+self.show_begin_line, 6, '♫  ♪ ♫  ♪', curses.color_pair(3))
        self.screen.addstr(1+self.show_begin_line, 17, song_name + ' - ' + artist + ' < ' + album_name + ' >', curses.color_pair(4))
        self.screen.refresh()     

    def build_loading(self,i=1):
        if i==1:
            self.screen.addstr(6+self.show_begin_line, 16, '享受高品质音乐，loading...', curses.color_pair(1))
        elif i==2:
            self.screen.addstr(6+self.show_begin_line, 16, 'loading...', curses.color_pair(3))
        self.screen.refresh()        

    def build_menu(self, datatype, title, datalist, offset, index, step,album_name_P=False):
        # keep playing info in line 1
        curses.noecho()
        self.screen.move(4+self.show_begin_line,1)
        self.screen.clrtobot()
        if datatype=='main':  #调整标题位置
            self.screen.addstr(4+self.show_begin_line, 19, title, curses.color_pair(1))
        else:
            self.screen.addstr(4+self.show_begin_line, 9, title, curses.color_pair(1))

        if len(datalist) == 0:
            self.screen.addstr(8+self.show_begin_line, 19, '这里什么都没有 -，-')

        else:
            if datatype == 'main':
                for i in range( offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 16, '-> ' + str(i) + '. ' + datalist[i], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 19, str(i) + '. ' + datalist[i])

            elif datatype == 'songs':
                for i in range(offset, min( len(datalist), offset+step) ):
                    # this item is focus
                    if album_name_P:   #显示专辑名 
                        if i == index:
                            self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i]['song_name'] + '  -  ' + datalist[i]['artist'] + '  < ' + datalist[i]['album_name'] + ' >', curses.color_pair(2))
                        else:
                            self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i]['song_name'] + '  -  ' + datalist[i]['artist'] + '  < ' + datalist[i]['album_name'] + ' >')
                    else:  #不显示专辑名
                        if i==index:
                            self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i]['song_name'] + '  -  ' + datalist[i]['artist'], curses.color_pair(2))
                        else:
                            self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i]['song_name'] + '  -  ' + datalist[i]['artist'] )

            
            elif datatype == 'artists':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 16, '-> ' + str(i) + '. ' + datalist[i]['artists_name'] + '   -   ' + str(datalist[i]['alias']), curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 19, str(i) + '. ' + datalist[i]['artists_name'] + '   -   ' + datalist[i]['alias'])

            elif datatype == 'albums':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i]['albums_name'] + '   -   ' + datalist[i]['artists_name'], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i]['albums_name'] + '   -   ' + datalist[i]['artists_name'])

            elif datatype == 'playlists':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i]['title'], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i]['title'])


            elif datatype == 'top_playlists':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i]['playlists_name'] + '   -   ' + datalist[i]['creator_name'], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i]['playlists_name'] + '   -   ' + datalist[i]['creator_name'])

            elif datatype == 'toplists': #排行榜榜名
                for i in range(offset, min(len(datalist),offset+step)):
                    if i == index:
                        self.screen.addstr(i-offset+8+self.show_begin_line, 7, '->' + str(i) + '. ' + datalist[i], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset + 8 + self.show_begin_line, 9 ,str(i) + '. ' + datalist[i])


            elif datatype == 'playlist_classes' or datatype == 'playlist_class_detail':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i])

            elif datatype == 'djchannels':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 6, '-> ' + str(i) + '. ' + datalist[i]['song_name'], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 9, str(i) + '. ' + datalist[i]['song_name'])                

            elif datatype == 'help':
                for i in range(offset, min( len(datalist), offset+step) ):
                    if i == index:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 16, '-> ' + str(i) + '. \'' + datalist[i][0].upper() + '\'   ' + datalist[i][1] + '   ' + datalist[i][2], curses.color_pair(2))
                    else:
                        self.screen.addstr(i - offset +8+self.show_begin_line, 19, str(i) + '. \'' + datalist[i][0].upper() + '\'   ' + datalist[i][1] + '   ' + datalist[i][2])                
                self.screen.addstr(18+self.show_begin_line, 6, 'MusicBox 基于Python，所有版权音乐来源于网易，本地不做任何保存')
                self.screen.addstr(21+self.show_begin_line, 6, '按 [G] 到 Github 了解更多信息，帮助改进，或者Star表示支持~~')

        self.screen.refresh()    

    def build_search(self, stype):
        netease = self.netease
        if stype == 'songs':
            song_name = self.get_param('搜索歌曲：')
            try:
                data = netease.search(song_name, stype=1)
                song_ids = []
                if 'songs' in data['result']:
                    if 'mp3Url' in data['result']['songs']:
                        songs = data['result']['songs']

                    # if search song result do not has mp3Url
                    # send ids to get mp3Url
                    else:
                        for i in range(0, len(data['result']['songs']) ):
                            song_ids.append( data['result']['songs'][i]['id'] )
                        songs = netease.songs_detail(song_ids)
                    return netease.dig_info(songs, 'songs')
            except:
                return []
        
        elif stype == 'artists':
            artist_name = self.get_param('搜索艺术家：')
            try:
                data = netease.search(artist_name, stype=100)
                if 'artists' in data['result']:
                    artists = data['result']['artists']
                    return netease.dig_info(artists, 'artists')
            except:
                return []

        elif stype == 'albums':
            artist_name = self.get_param('搜索专辑：')
            try:
                data = netease.search(artist_name, stype=10)
                if 'albums' in data['result']:
                    albums = data['result']['albums']
                    return netease.dig_info(albums, 'albums')
            except:
                return []

        elif stype == 'search_playlist':
            artist_name = self.get_param('搜索网易精选集：')
            try:
                data = netease.search(artist_name, stype=1000)
                if 'playlists' in data['result']:
                    playlists = data['result']['playlists']
                    return netease.dig_info(playlists, 'top_playlists')
            except:
                return []

        return []

    def build_search_menu(self):
        self.screen.move(4+self.show_begin_line,1)
        self.screen.clrtobot()
        self.screen.addstr(8+self.show_begin_line, 19, '选择搜索类型:', curses.color_pair(1))
        self.screen.addstr(10+self.show_begin_line,19, '[1] 歌曲')
        self.screen.addstr(11+self.show_begin_line,19, '[2] 艺术家')
        self.screen.addstr(12+self.show_begin_line,19, '[3] 专辑')
        self.screen.addstr(13+self.show_begin_line,19, '[4] 网易精选集')
        self.screen.addstr(16+self.show_begin_line,19, '请键入对应数字:', curses.color_pair(2))
        self.screen.refresh()
        x = self.screen.getch()
        return x

    def build_login(self):
        self.screen.move(7+self.show_begin_line,1)
        self.screen.clrtobot()
        curses.noecho()
        info = self.get_param('请输入登录信息(q or Q 退出登陆)， e.g: john@163.com 123456')
        if str(info) in ('q','Q'):
            return -1
        account = info.split(' ')
        if len(account) != 2:
            return self.build_login()
        login_info = self.netease.login(account[0], account[1])
        if login_info['code'] != 200:
            x = self.build_login_error()
            if x == ord('1'):
               return self.build_login()
            else:
                return -1
        else:
            return [login_info, account]        

    def build_login_error(self):
        self.screen.move(4+self.show_begin_line,1)
        self.screen.clrtobot()
        self.screen.addstr(8+self.show_begin_line, 19, '艾玛，登录信息好像不对呢 (O_O)#', curses.color_pair(1))
        self.screen.addstr(10+self.show_begin_line,19, '[1] 再试一次')
        self.screen.addstr(11+self.show_begin_line,19, '[2] 稍后再试')
        self.screen.addstr(14+self.show_begin_line,19, '请键入对应数字:', curses.color_pair(2))
        self.screen.refresh()
        x = self.screen.getch()
        return x

    def get_param(self, prompt_string):
          # keep playing info in line 1        
        curses.echo()
        self.screen.move(4+self.show_begin_line,1)
        self.screen.clrtobot()
        self.screen.addstr(5+self.show_begin_line, 3, prompt_string, curses.color_pair(1))
        self.screen.refresh()
        info = self.screen.getstr(10, 19, 60)
        if info.strip() is '':
            return self.get_param(prompt_string)
        else:
            return info

    def progress_bar(self,time_now,length):  #进度条
        cols=int(self.COLS)-18
        time_now=int(ceil(float(time_now)))
        length=int(ceil(float(length)))
        if time_now>length:
            time_now=length
        surplus=length-time_now
        if length!=0 and length!=0:
            t_now="%2d:%02d" % (int(time_now//60),int(time_now%60))
            t_surplus="%2d:%02d" % (int(surplus//60),int(surplus%60))
            dutyfactor_1=int(ceil(float(time_now)/length*cols))
            line=t_now+' '+'*'*dutyfactor_1+'>'+'-'*(cols-dutyfactor_1)+' '+t_surplus
            self.screen.addstr(20+self.show_begin_line,2,line,curses.color_pair(3))
            self.screen.refresh()


    def notifySend(self,name,artist,other=''):   #发送桌面通知
        s=other+name+' -- <'+artist+'>'
        subprocess.call(['notify-send',s])
