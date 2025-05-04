#bomb_audio.py will handle all audio files and sounds for the bomb game
#this file will have several subroutines that will be imported into bomb_phases.py
#for playing sounds

#imports
import pygame
import os
from time import sleep

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
    sound = pygame.mixer.Sound(trophies)
    # Play the sound
    sound.play()
    #set a timer to stop the sound after 5 seconds
    pygame.time.set_timer(pygame.USEREVENT, 5000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                #stop the sound and cancel the timer
                sound.stop()
                pygame.time.set_timer(pygame.USEREVENT, 0)  #cancel the timer
                running = False

