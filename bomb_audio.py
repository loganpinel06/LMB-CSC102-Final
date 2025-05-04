#bomb_audio.py will handle all audio files and sounds for the bomb game
#this file will have several subroutines that will be imported into bomb_phases.py
#for playing sounds

#imports
import pygame
import os
import time
import threading

#create a global variable for the bomb audio directory
MEDIA = "/home/spartans/LMB-CSC142-Final/media"

#create a subroutine to initialize the pygame mixer
def initPygame():
    pygame.init()
    pygame.mixer.init()

#create a subroutine for the bootup sound
def bootupSound():
    #get the mp3 file path
    trophies = os.path.join(MEDIA, "trophiesdrake.mp3")
    #load the mixer
    pygame.mixer.music.load(trophies)
    #stop the music after 14 seconds
    pygame.mixer.music.play(loops=0, start=0.0)
    
    #timer so we can stop the sound after 14 seconds
    def stopMusic():
        time.sleep(14)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    
    #start a thread to stop the music after 14 seconds
    threading.Thread(target=stopMusic).start()

