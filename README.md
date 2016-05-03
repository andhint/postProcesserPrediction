# postProcesserPrediction
A python script that predicts what post processing techniques were done to an image. Uses Python 2.7 and 
the <a href="http://opencv.org/">OpenCV</a> library for image processing. This script requires that numpy, 
cv2, and matplotlib libraries are installed.

There are number of test images included in the repository. To select which one is loaded either comment/uncomment 
the line reading in the image in main() ( img = cv2.imread('image.jpg') ) or change the name of the file. 

So far the script can find clipping in the blacks and whites, crushed blacks, and lifted blacks. To find out how each one of these is done refer to the comments in the script under the appropriate function. Determining split 
toning and getting a HSL(Hue Saturation and Luminance) distribution for an image are up next.
