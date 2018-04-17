#!/usr/bin/env python

'''
ballpit code - moving average background subtraction, hotspots, sounds
'''

import cv2
import video
import sys
import numpy as np
from Hotspot import Hotspot
from os import listdir
from os.path import isfile, join
import sounddevice as sd
import soundfile as sf

hist=5
wid=5
no_sounds=8
no=0
dirname='/home/hannah/coding/ballpit/sounds/'

hotspots=[]

# mouse callback function
def add_hotspot(event,x,y,flags,param):
    global no
    if event == cv2.EVENT_LBUTTONUP:
        if (no<no_sounds):
            print(x,y,no)
            hotspots[no].update_location(x,y)
            no+=1

if __name__ == '__main__':
    print(__doc__)

# if we have a filename let's have a go at opening that...
    try: fn = sys.argv[1]
    except: fn = 0
    def nothing(*argv):
        pass


    
    soundfiles = [join(dirname,f) for f in listdir(dirname) if isfile(join(dirname,f))] 
    
    no_sounds=len(soundfiles)
    print(no_sounds)
    print(soundfiles)
    sounds = []
    fs = []
    for i in range (no_sounds):
         x=Hotspot(hist,wid) 
         hotspots.append(x)
         s,f =sf.read(soundfiles[i])
         sounds.append(s)
         fs.append(f)
         sd.play(sounds[i], fs[i])

# gizza window with a trackbar on it
    cv2.namedWindow('bgmodel')
    cv2.namedWindow('foregound')
    cv2.createTrackbar('Size of buffer', 'bgmodel', 110, 500, nothing)
    cv2.createTrackbar('Difference threshold', 'bgmodel', 10, 200, nothing)

    cv2.setMouseCallback('bgmodel',add_hotspot)
    n=0
# gizza videocapture object
    cap = video.create_capture(fn)

    flag, im = cap.read()
    img=cv2.flip(im,1)
    movingaverage=np.float32(img)
    while True:

#read a frame from the video capture obj

        flag, im = cap.read()
           
        img=cv2.flip(im,1)

        fbuffer=cv2.getTrackbarPos('Size of buffer', 'bgmodel')
#let's deal with that pesky zero case before we divide by fbuffer
        if fbuffer==0:
            fbuffer=1
        alpha=float(1.0/fbuffer) 
        cv2.accumulateWeighted(img,movingaverage,alpha) 

# do the drawing stuff
        res=cv2.convertScaleAbs(movingaverage)
# show the background model 
        cv2.imshow('bgmodel', res)


# take the absolute difference of the background and the input
        difference_img = cv2.absdiff(res, img)
# make that greyscale

        grey_difference_img = cv2.cvtColor(difference_img, cv2.COLOR_BGR2GRAY)
# threshold it to get a motion mask 
        difference_thresh=cv2.getTrackbarPos('Difference threshold', 'bgmodel')
        ret,th1 = cv2.threshold(grey_difference_img,difference_thresh,255,cv2.THRESH_BINARY)
        fgimg=cv2.merge((th1,th1,th1))
        intimg=cv2.integral(th1)
        i=0
        for h in hotspots:
           cv2.rectangle(fgimg,h.tl,h.br,(255,0,0),3)
           if (h.is_moving(intimg)):
               cv2.rectangle(fgimg,h.tl,h.br,(0,255,0),3)
               sd.play(sounds[i])
           i=i+1
        cv2.imshow('foregound',fgimg)
        n+=1
 

#open cv window management/redraw stuff 
        ch = cv2.waitKey(5)
        if ch == 27:
            break
    cv2.destroyAllWindows()
