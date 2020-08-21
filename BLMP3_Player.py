#!/usr/bin/env python3
import RPi.GPIO as GPIO
import glob
import subprocess
import os, signal
import time
import random
from random import shuffle

#v1.0

# use coinslot, set to 1 to use, 0 to disable
use_coinslot = 1

# define 20 button GPIO pins used
opins = (29,31,33,35,37)
ipins = (32,36,38,40)

# define 20 LED GPIO pins used
apins = (11,13,15,19,21)
bpins = (8,10,24,26)

# buttons connections
coinslot  = 12
shuffler  = 16
stop      = 18
shutdown  = 22

# LEDS
LED1 = 23 # CABINET LED
LED2 = 5  # COIN LED

# define letters
letters = ("A","B","C","D","E","F","G","H","I","J")

# setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
for count in range(0,4):
    GPIO.setup(ipins[count],GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for count in range(0,5):
    GPIO.setup(opins[count],GPIO.OUT)
    GPIO.output(opins[count],GPIO.LOW)
for count in range(0,5):
    GPIO.setup(apins[count],GPIO.OUT)
    GPIO.output(apins[count],GPIO.LOW)
for count in range(0,4):
    GPIO.setup(bpins[count],GPIO.OUT)
    GPIO.output(bpins[count],GPIO.LOW)
GPIO.setup(coinslot,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(shuffler,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(shutdown,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
GPIO.output(LED1,GPIO.LOW)

# set starting variables
X = Y = -1
coin_det = 0
time_start = 0
Con_pressed = 0
Con_Play = 0
Play = 0
trace = 1
Con_shuffle = 0

# find tracks
tracks = glob.glob("/home/pi/Music/*.mp3")
tracks.sort()

# test leds
if trace == 1:
    print ("Testing LEDs...")
for count in range(0,5):
    GPIO.output(apins[count],GPIO.HIGH)
    for count in range(0,4):
        GPIO.output(bpins[count],GPIO.LOW)
for j in range(0,4):
    GPIO.output(bpins[j],GPIO.HIGH)
    for k in range(0,5):
        GPIO.output(apins[k],GPIO.LOW)
        time.sleep(0.07)
        GPIO.output(apins[k],GPIO.HIGH)
    GPIO.output(bpins[j],GPIO.LOW)
GPIO.output(LED1,GPIO.HIGH)
time.sleep(0.1)
GPIO.output(LED1,GPIO.LOW)
GPIO.output(LED2,GPIO.HIGH)
time.sleep(0.1)
GPIO.output(LED2,GPIO.LOW)
time.sleep(0.1)
GPIO.output(LED1,GPIO.HIGH) # turn CABINET LED ON
GPIO.output(LED2,GPIO.LOW)  # turn LED2 OFF

if use_coinslot == 1 and trace == 1:
    print ("Insert a coin")

def key_check():
    global ipins,opins,K,time_start,kmap,Con_Play,letters,Z,p,X,Y,tracks,coin_det,Con_pressed,oldj,oldk,apins,bpins,trace
    for e in range(0,5):
        GPIO.output(opins[e],GPIO.HIGH)
        for f in range(0,4):
            if GPIO.input(ipins[f]) == 1:
                K =(f*5) + e
                j = e
                k = f
        GPIO.output(opins[e],GPIO.LOW)
    if K != -1:
        time_start = time.time()
        if Con_Play == 0 and Play == 0:
            
            for count in range(0,5):
                GPIO.output(apins[count],GPIO.HIGH)
            for count in range(0,4):
                GPIO.output(bpins[count],GPIO.LOW)
            GPIO.output(apins[j],GPIO.LOW)
            GPIO.output(bpins[k],GPIO.HIGH)
        if K >  9 and trace == 1:
            print (str(K-9),"pressed")
        elif K < 10 and trace == 1:
            print (str(letters[K]),"pressed")
        GPIO.output(opins[j],GPIO.HIGH)
        while GPIO.input(ipins[k]) == 1 and coin_det == 1:
            if Con_Play == 0:
                if time.time() - time_start > 5 and K == 1:
                    Con_Play = 1
                    if trace == 1:
                        print ("Continuous Play Mode")
                    for count in range(0,5):
                        GPIO.output(apins[count],GPIO.HIGH)
                    for count in range(0,4):
                        GPIO.output(bpins[count],GPIO.LOW)
            time.sleep(0.1)
        time_start = time.time()

while True:

    # wait for a coin
    if use_coinslot == 1:
        while GPIO.input(coinslot) == 1 and coin_det == 0:
            time.sleep (.25)

    if GPIO.input(shutdown) == 0:
        GPIO.output(LED1,GPIO.LOW)
        if trace == 1:
            print ("Goodbye!")
        os.system("sudo shutdown -h now")

    # coin detected, start timer       
    if coin_det == 0:
        if trace == 1:
            if use_coinslot == 1:
                print ("Coin detected")
        time_start = time.time()
        GPIO.output(LED2,GPIO.HIGH) # turn LED2 ON
        coin_det = 1

    # if no activity for 60 seconds, cancel coin detected   
    if time.time() - time_start > 60 and X == -1:
        coin_det = 0
        GPIO.output(LED2,GPIO.LOW) # turn LED2 OFF
        for count in range(0,5):
             GPIO.output(apins[count],GPIO.HIGH)
        for count in range(0,4):
             GPIO.output(bpins[count],GPIO.LOW)
        if trace == 1:
            print ("Sorry timed out")
            if use_coinslot == 1:
                print ("Insert another coin !")
    
    time.sleep(0.1)
        
    # check for a letter press
    if X == -1 and coin_det == 1:
        K = -1
        key_check()
        if K < 10:
            X = K
        else:
            X = -1
            for count in range(0,5):
                GPIO.output(apins[count],GPIO.HIGH)
            for count in range(0,4):
                GPIO.output(bpins[count],GPIO.LOW)

    # no number pressed within 5 seconds of a letter, cancel letter
    if X != -1 and time.time() - time_start > 5:
        X = -1
        GPIO.output(LED2,GPIO.HIGH) # turn LED2 ON
        for count in range(0,5):
            GPIO.output(apins[count],GPIO.HIGH)
        for count in range(0,4):
            GPIO.output(bpins[count],GPIO.LOW)
        if trace == 1:
            print ("Timed out waiting for a number, choose a letter again")
           
    # check for a number press
    if X != -1 and Y == -1 and coin_det == 1 and Con_Play == 0:
        K = -1
        key_check()
        if K > 9 and K < 21:
            Y = K
            Play = 1
           
    # if letter and number pressed play a song
    if Play == 1:
        GPIO.output(LED2,GPIO.LOW)
        # calculate track number from numbers pressed
        Z = (X*10 + (Y - 9)) - 1
        m = int(Z/50)
        o = int(Z/10) - (m*5)
        r = Z - (int(Z/10)*10)
        s = int(r/5) + 2
        t = r - (int(r/5)*5)
        blink = 0
        if Z < len(tracks):
            if trace == 1:
                print ("Playing Track: ", letters[X] + str(Y-9), tracks[Z] )
            rpistr = "mplayer " + '"' + tracks[Z] + '"'
            p = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
            # check if track still playing
            poll = p.poll()
            while poll == None:                       # track still playing
                GPIO.output(LED2,GPIO.LOW)            # turn LED2 OFF
                for count in range(0,5):
                    GPIO.output(apins[count],GPIO.HIGH)
                for count in range(0,4):
                    GPIO.output(bpins[count],GPIO.LOW)
                if blink == 0 :
                    GPIO.output(apins[o],GPIO.LOW)
                    GPIO.output(bpins[m],GPIO.HIGH)
                    blink = 1
                else:
                    GPIO.output(apins[t],GPIO.LOW)
                    GPIO.output(bpins[s],GPIO.HIGH)
                    blink = 0
                time.sleep(0.01)
                if  GPIO.input(stop) == 0:
                    if trace == 1:
                        print ("Track stopped")
                    os.killpg(p.pid, signal.SIGTERM)
                    time.sleep(0.5)
                    for count in range(0,5):
                        GPIO.output(apins[count],GPIO.HIGH)
                    for count in range(0,4):
                        GPIO.output(bpins[count],GPIO.LOW)
                if  GPIO.input(shutdown) == 0:
                    GPIO.output(LED1,GPIO.LOW)        # turn LED1 OFF
                    if trace == 1:
                        print ("Goodbye!")
                    os.killpg(p.pid, signal.SIGTERM)
                    time.sleep(0.5)
                    os.system("sudo shutdown -h now")
                    
                poll = p.poll()
            if trace == 1:
                print ("Track Finished")
            for count in range(0,5):
                GPIO.output(apins[count],GPIO.HIGH)
            for count in range(0,4):
                GPIO.output(bpins[count],GPIO.LOW)
            coin_det = 0
            X = -1
            Y = -1
            Play = 0
            if trace == 1:
                if use_coinslot == 1:
                    print ("Insert another coin")
        else:
            if trace == 1:
                print ("No track found")
            coin_det = 0
            X = -1
            Y = -1
            Play = 0
            if trace == 1:
                if use_coinslot == 1:
                    print ("Insert another coin")
                

    # Con_Play = 1 so continuous play mode...
    if Con_Play == 1:
        nums = [0] * len(tracks)
        for Z in range(0,len(tracks)):
            nums[Z] = Z
        # shuffle tracks, if selected.
        if Con_shuffle == 1:
            if trace == 1:
                print ("Shuffled tracks")
            shuffle(nums)
        GPIO.output(LED2,GPIO.LOW)
        Z = 0
        blink = 0
        skip = 0
        while Con_Play == 1 :
            if nums[Z] < 100:
                q = int(nums[Z] / 10)
                r = (nums[Z] - (q * 10)) + 1
                if trace == 1:
                    print ("Playing Track: ",letters[q] + str(r),tracks[nums[Z]])
            elif trace == 1:
                print ("Playing Track: ",str(nums[Z]+1),tracks[nums[Z]])
            rpistr = "mplayer " + '"' + tracks[nums[Z]] + '"'
            p = subprocess.Popen(rpistr, shell=True, preexec_fn=os.setsid)
            m = int(nums[Z]/50)
            o = int(nums[Z]/10) - (m*5)
            r = nums[Z] - (int(nums[Z]/10)*10)
            s = int(r/5) + 2
            t = r - (int(r/5)*5)
            # check if track still playing
            poll = p.poll()
            while poll == None:                         # track still playing
                GPIO.output(LED2,GPIO.LOW)
                time.sleep(0.01)
                for count in range(0,5):
                    GPIO.output(apins[count],GPIO.HIGH)
                for count in range(0,4):
                    GPIO.output(bpins[count],GPIO.LOW)
                if nums[Z] < 100:
                    if blink == 0:
                        GPIO.output(apins[o],GPIO.LOW)
                        GPIO.output(bpins[m],GPIO.HIGH)
                        blink = 1
                    else:
                        GPIO.output(apins[t],GPIO.LOW)
                        GPIO.output(bpins[s],GPIO.HIGH)
                        blink = 0
                K = -1
                key_check()
                if  K == 0:           # Previous track     (A pressed)
                    if trace == 1:
                        print ("Previous Track...")
                    os.killpg(p.pid, signal.SIGTERM)
                    time.sleep(0.5)
                    Z -= 1
                    skip = 1
                if  K == 2:           # Next Track         (C pressed)
                    if trace == 1:
                        print ("Next Track...")
                    os.killpg(p.pid, signal.SIGTERM)
                    time.sleep(0.5)
                if  K == 3:           # 10 Track Backwards (D pressed)
                    if trace == 1:
                        print ("Skip 10 Track backwards...")
                    os.killpg(p.pid, signal.SIGTERM)
                    time.sleep(0.5)
                    Z -= 10
                    skip = 1
                if  K == 4:           # 10 Track Forward   (E pressed)
                    if trace == 1:
                        print ("Skip 10 Track forward...")
                    os.killpg(p.pid, signal.SIGTERM)
                    time.sleep(0.5)
                    Z += 10
                    skip = 1
                if  GPIO.input(stop) == 0:              # Exiting Continuous Play (if STOP pressed > 5 secs)
                    timer1 = time.time()
                    while GPIO.input(stop) == 0:
                        if time.time() - timer1 > 5:
                            if Con_Play == 1:
                                timer1 = time.time()
                                if trace == 1:
                                    print ("Track stopped")
                                os.killpg(p.pid, signal.SIGTERM)
                                time.sleep(0.5)
                                Con_Play = 0
                                if trace == 1:
                                    print ("Exiting Continuous Play...")
                                    print ("Choose a Letter")
                                X = -1
                                Y = -1
                                for count in range(0,5):
                                    GPIO.output(apins[count],GPIO.HIGH)
                                for count in range(0,4):
                                    GPIO.output(bpins[count],GPIO.LOW)
                if GPIO.input(shuffler) == 0 or K == 19:
                    Con_shuffle = 1
                    shuffle(nums)
                    if trace == 1:
                        print ("Shuffle set")
                if  GPIO.input(shutdown) == 0:          # shutdown
                    GPIO.output(LED1,GPIO.LOW)
                    if trace == 1:
                        print ("Goodbye!")
                    os.killpg(p.pid, signal.SIGTERM)
                    os.system("sudo shutdown -h now")
                poll = p.poll()
            if skip == 0:
                Z += 1
            skip = 0
            if Z > len(tracks) - 1:
                Z = Z - len(tracks)
            if Z < 0:
                Z = len(tracks) + Z



            
