#bomb_audio.py will handle all audio files and sounds for the bomb game
#this file will have several subroutines that will be imported into bomb_phases.py
#for playing sounds

#imports
import pygame
import os
import time
import threading

#create a global variable for the bomb audio directory
MEDIA = "/home/spartans/LMB-CSC102-Final/media"

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
    #set the volume to 0.7
    pygame.mixer.music.set_volume(0.7)
    #play the music
    pygame.mixer.music.play(loops=0, start=0.0)
    
    #timer so we can stop the sound after 15 seconds
    def stopMusic():
        time.sleep(15)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    
    #start a thread to stop the music after 15 seconds
    threading.Thread(target=stopMusic).start()

#subroutine for the wires sound
def wiresSound():
    #get the mp3 file path
    bang = os.path.join(MEDIA, "bang.mp3")
    #load the mixer
    sound = pygame.mixer.Sound(bang)
    #set the volume to 0.7
    sound.set_volume(0.7)
    #play the sound
    sound.play()

#subroutine for the button sound
def buttonSound():
    #get the mp3 file path
    swish = os.path.join(MEDIA, "swish.mp3")
    #load the mixer
    sound = pygame.mixer.Sound(swish)
    #play the sound
    sound.play()

#subroutine for the keypad sound
def keypadSound():
    #get the mp3 file path
    greenbean = os.path.join(MEDIA, "greenbean.mp3")
    #load the mixer
    sound = pygame.mixer.Sound(greenbean)
    #set the volume to 0.7
    sound.set_volume(0.7)
    #play the sound
    sound.play()

#subroutine for the toggles sound
def togglesSound():
    #get the mp3 file path
    money = os.path.join(MEDIA, "money.mp3")
    #load the mixer
    sound = pygame.mixer.Sound(money)
    #play the sound
    sound.play()

#subroutine for the explosion sound
def explosionSound():
    #get the mp3 file path
    explosion = os.path.join(MEDIA, "bombexplode.mp3")
    #load the mixer
    sound = pygame.mixer.Sound(explosion)
    #play the sound
    sound.play()
    #stop the sound early
    sound.stop()