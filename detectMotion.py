#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import random
import pygame
from pygame import mixer
from os import listdir
from os.path import isfile, join


#Audio SETUP
audioPath = '/home/pi/Desktop/AudioFiles'
audioFiles = [f for f in listdir(audioPath) if isfile(join(audioPath, f))]
lastPlayed = []

#Mixer SETUP
mixer.init()

#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
        if GPIO.input(channel) and mixer.music.get_busy() != 1:
                print("Movement Detected!")
                selection = random.choice(audioFiles)
                mixer.music.load(audioPath + '/' + selection)
                mixer.music.play()
                if len(lastPlayed) != 0: 
                    audioFiles.append(lastPlayed[0]) #readd previously played song
                    lastPlayed.remove(lastPlayed[0]) #clear last played list
                lastPlayed.append(selection) # add new last played song
                audioFiles.remove(selection) # remove new from next selection
                
        else:
                print("Movement Detected2!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

# infinite loop
while True:
        time.sleep(1)
