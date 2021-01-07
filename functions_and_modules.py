########################################################### IMPORTS ###############################################################################
import matplotlib
matplotlib.use('Agg')
import time
from time import sleep
import os
import sys
import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
import gpiozero as io
from gpiozero.tones import Tone 
from smbus2 import SMBusWrapper, i2c_msg               #for i2c devices
import Adafruit_DHT
#import Adafruit_Python_SSD1306   #oled if necessary
from configuration import *
#import tendo





########################################################### FUNCTIONS ###############################################################################

def gettimestamp():
        timestamp = time.strftime("%H:%M:%S")
        return timestamp

def gethours():
    hours = time.strftime("%H")
    return int(hours)

def getminutes():
    minutes = time.strftime("%M")
    return int(minutes)

def DHT_read(sensor, pin):
    print('reading DHT, this takes some time...')
    sleep(2)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    sleep(2)
    return (humidity, temperature)
    
def beep(buzzer):
    buzzer.play(Tone(500.0)) # Hz
    sleep(0.15)
    buzzer.stop()
    sleep(0.15)
    buzzer.play(Tone(500.0)) # Hz
    sleep(0.15)
    buzzer.stop()


    

def set_starttime():
        start_time = time.time()
        return start_time

def time_since_start(start_time):
        return((time.time() - start_time))

def i2c_iAq_read(address):
    """
     Read 9 bits from iAq (default adress 90)
     returns CO2, R, TVOC
    """
    with SMBusWrapper(1) as bus:
        # Read 64 bytes from address 80
        msg = i2c_msg.read(address, 9)
        bus.i2c_rdwr(msg)
    byte = []

    for value in msg:
        byte.append(value)

    CO2 = byte[0] * 2 ** 8 + byte[1]
    R = byte[4] * 2 ** 16 + byte[5] * 2 ** 8 + byte[6]
    TVOC = byte[7] * 2 ** 8 + byte[8]

    return (CO2, TVOC)

