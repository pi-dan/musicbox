#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: omi
# @Date:   2014-07-15 15:48:27
# @Last Modified by:   pi-dan
# @Last Modified time: 2015-01-08 18:02:00


'''
网易云音乐 Player
'''
# Let's make some noise

import subprocess
import threading
import time
import os
from ui import Ui
import tempfile


# carousel x in [left, right]
carousel = lambda left, right, x: left if (x>right) else (right if x<left else x)


class Player:

    def __init__(self):
        self.ui = Ui()
        self.datatype = 'songs'
        self.popen_handler = None
        # flag stop, prevent thread start
        self.playing_flag = False
        self.pause_flag = False
        self.songs = []
        self.idx = 0
        self.next_music_p=False  #播放下一曲标志
        self.stop_sub=False  #结束自动播放下一曲,手动选择播放``
        self.mplayer_controller=os.path.join(tempfile.mkdtemp(),'mplayer_controller')
        os.mkfifo(self.mplayer_controller)  #临时文件``

        

    def return_idx(self):
        return self.idx,self.playing_flag#,self.next_music_p

    def popen_recall(self, onExit, popenArgs):
        """
        Runs the given args in a subprocess.Popen, and then calls the function
        onExit when the subprocess completes.
        onExit is a callable object, and popenArgs is a lists/tuple of args that 
        would give to subprocess.Popen.
        """
        def runInThread(onExit, popenArgs):
            self.ui.notifySend(name=self.songs[self.idx]['song_name'],artist=self.songs[self.idx]['artist'])
            play_s='mplayer -quiet -slave -input file={fifo} \'{song_url}\' 2>&1'
            self.popen_handler = subprocess.Popen(play_s.format(fifo=self.mplayer_controller,song_url=popenArgs),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,bufsize=1)
            self.popen_handler.wait()
            if self.playing_flag and self.stop_sub==False:
                self.idx = carousel(0, len(self.songs)-1, self.idx+1 )
                #self.next_music_p= not self.next_music_p #对下一曲标志取反
                onExit()
            else:
                self.stop_sub=False
            return
        thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
        thread.start()
        # returns immediately after the thread starts
        return thread

    def recall(self):
        self.playing_flag = True
        item = self.songs[ self.idx ]
        self.ui.build_playinfo(item['song_name'], item['artist'], item['album_name'])
        self.popen_recall(self.recall, item['mp3_url'])

    def play(self, datatype, songs, idx):
        # if same playlists && idx --> same song :: pause/resume it
        self.datatype = datatype

        if datatype == 'songs' or datatype == 'djchannels':
            if idx == self.idx and songs == self.songs:
                if self.pause_flag:
                    self.resume()        
                else:
                    self.pause()

            else:    
                if datatype == 'songs' or datatype == 'djchannels':
                    self.songs = songs
                    self.idx = idx

                # if it's playing
                if self.playing_flag:
                    self.switch()

                # start new play
                else:
                    self.recall()
        # if current menu is not song, pause/resume
        else:
            if self.playing_flag:
                if self.pause_flag:
                    self.resume()
                else:
                    self.pause()
            else:
                pass

    # play another   
    def switch(self):
        self.stop()
        # wait process be killed
        time.sleep(0.01)
        self.recall()

    def stop(self):
        if self.playing_flag and self.popen_handler:
            self.playing_flag = False
            self.stop_sub=True
            subprocess.Popen('echo "quit" > {fifo}'.format(fifo=self.mplayer_controller),shell=True,stdin=subprocess.PIPE).wait()
            #self.popen_handler.kill()

    def pause(self):
        self.pause_flag = True
        #os.kill(self.popen_handler.pid, signal.SIGSTOP)
        subprocess.Popen('echo "pause" > {fifo}'.format(fifo=self.mplayer_controller),shell=True,stdin=subprocess.PIPE)
        item = self.songs[ self.idx ]
        self.ui.build_playinfo(item['song_name'], item['artist'], item['album_name'], pause=True)
        self.ui.notifySend(name=item['song_name'],artist=item['artist'],other='暂停-> ')
        


    def resume(self):
        self.pause_flag = False
        subprocess.Popen('echo "pause" > {fifo}'.format(fifo=self.mplayer_controller),shell=True,stdin=subprocess.PIPE)
        #os.kill(self.popen_handler.pid, signal.SIGCONT)
        item = self.songs[ self.idx ]
        self.ui.build_playinfo(item['song_name'], item['artist'], item['album_name'])
        self.ui.notifySend(name=item['song_name'],artist=item['artist'],other='播放-> ')

    def next(self):
        self.stop() 
        self.idx = carousel(0, len(self.songs)-1, self.idx+1 )
        self.recall()

    def prev(self):
        self.stop()
        self.idx = carousel(0, len(self.songs)-1, self.idx-1 )
        self.recall()

    def get_time_pos(self):  # 音乐的当前位置用秒表示，采用浮点数。
        subprocess.Popen('echo "get_time_pos" > {fifo}'.format(fifo=self.mplayer_controller),shell=True,stdin=subprocess.PIPE).wait()
        time_now=self.popen_handler.stdout.readline().decode('utf-8') 
        i=0
        while True:
            if 'ANS_TIME_POSITION=' in time_now:
                break
            elif i>20:
                subprocess.Popen('echo "get_time_pos" > {fifo}'.format(fifo=self.mplayer_controller),shell=True,stdin=subprocess.PIPE).wait()
                i=0
            else:
                i=i+1
                time_now=self.popen_handler.stdout.readline()##.decode('utf-8') 
        return time_now.split('=')[1].strip('\n')

    def get_time_length(self):
        subprocess.Popen('echo "get_time_length" > {fifo}'.format(fifo=self.mplayer_controller),shell=True).wait()
        time_length=self.popen_handler.stdout.readline()#.decode('utf-8')
        i=0
        while True:
            if 'ANS_LENGTH=' in time_length:
                break
            elif i>20:
                subprocess.Popen('echo "get_time_length" > {fifo}'.format(fifo=self.mplayer_controller),shell=True).wait()
                i=0
            else:
                i=i+1
                time_length=self.popen_handler.stdout.readline().decode('utf-8')
        return time_length.split('=')[1].strip('\n')
