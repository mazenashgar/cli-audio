"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time

import os
import CLI_Audio_Exception

class Player:

    playingNow = False #variable set to false
    trackPlaying = ""
    mediaFiles = os.listdir("media")
    
    def __init__(self): #constructor method for the class
        self.currentSong = "Nothing playing."
        self.paused = True
        self.position = 0

    def getCurrentSong(self):
        if self.playingNow == True: #if a song is playing
            if self.stream.is_stopped() or self.paused == True: #if song is stopped or paused
                self.currentSong = "Nothing playing." #display string
                return self.currentSong #string message returned

    def pause(self):
        if self.paused == False: #if a song is not paused
            self.paused = True #set paused to true
            self.stream.stop_stream() #pause the song
            #self.currentSong = "Nothing playing."
        else: #if a song is paused
            self.paused = False #set paused to false
            self.stream.start_stream() #start playing song
            self.currentSong = self.trackPlaying #display name of current song playing

    def play(self, track):
        pathWithExt = track + '.wav'
        if pathWithExt not in self.mediaFiles:
                raise CLI_Audio_Exception.CLI_Audio_File_Exception
        self.paused = False
        self.currentSong = track
        self.trackPlaying = track
        track = './media/' + track + '.wav'
        self.wf = wave.open(track, 'rb') #acquire track

        # instantiate PyAudio
        self.p = pyaudio.PyAudio()

        # open self.stream using callback (
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                stream_callback=self.callback)

        # start the self.stream
        self.stream.start_stream()
        self.playingNow = True
    
    #method defined for stop playing song
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()

        self.p.terminate() 
    
    #method defined for replaying song
    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

