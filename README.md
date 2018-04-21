# ballpit

Hacky set of python scripts which (using pygame and OpenCV) takes a webcam feed and a directory full of audio files, lets you click on the webcam image to set "Hotspots" in the visual field, detects motion in those hotspots and plays a sound when the hotspot is activated.

The code 
* reads the directory listing, 
* counts how many soundfiles there are,
* sets the pygame mixer to have the right number of channels so you can play multiple sounds at once,
* reads the sounds into pygame objects,
* enters a video loop where the camera feed is read continually

In the camera loop...
* a moving average background model is maintained, based on a sliding window
* this is displayed to the user in one video preview
* motion is detected by subtracting the current frame from the background model
* this is displayed to the user in the other video preview window

## Setting the hotspots
If you click on the background model, it'll add a hotspot at that location. You can click as many times as there are sound files in your "sounds" directory

## Using the program

Wave your arms and bang the drums

# All I want for christmas is a drum kit ball pit

If you are feeling ambitious, point the camera at a ball pit.

[https://www.youtube.com/watch?v=GhtPAVvYItE]


