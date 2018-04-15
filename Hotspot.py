
import cv2
import video
import sys
import numpy as np

class Hotspot:
   x=0
   y=0
   tl=(0,0)
   br=(0,0)
#keep track of moving or not for a couple of frames
   recent_history=[]
   history_length=5
   spot_width=5

   def __init__(s, history, sw):
#initialise history loop to false with the right no of entries 
       s.history_length=history
       s.recent_history=[False]*s.history_length
       s.spot_width=sw

   def update_location(s, nx, ny):
       s.x=nx
       s.y=ny 
       s.tl=(nx-s.spot_width,ny-s.spot_width)
       s.br=(nx+s.spot_width,ny+s.spot_width)

   def is_moving(s, image):
       maxval=2*s.spot_width*2*s.spot_width*255;
       for i in range(s.history_length-1):
	   s.recent_history[i]=s.recent_history[i+1]
       print(maxval)
       sum_box= image[s.br[1]][s.br[0]] + image[s.tl[1]][s.tl[0]] \
           - image[s.tl[1]][s.br[0]] - image[s.br[1]][s.tl[0]]
       print(sum_box)
       if (sum_box > (maxval-50)):
           s.recent_history[s.history_length-1]=True
       else:
           s.recent_history[s.history_length-1]=False
       ret_val=True
       for i in range(s.history_length):
           if (s.recent_history[i]==False):
               ret_val=False
       return (ret_val)

