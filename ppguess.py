import numpy as np
import cv2
from matplotlib import pyplot as plt
import colorsys


###########################################################################################
###########   PLOTTING FUNCTIONS  #########################################################
###########################################################################################

def plotHist(hist):
	# Plots histogram of given histogram array data
	#
	# hist : array of histogram array data

	color = ('blue','green','red','black')
	for i,col in enumerate(color):
		plt.plot(hist[i],color = col)
		plt.xlim([0,256])
	plt.show()

def plotDiff(hist):
	# Plots derivative of histogram for total data
	#
	# hist : array of histogram array data

	arr = np.diff(histToArray(hist[3]))
	plt.plot(np.absolute(arr),color = 'black')
	plt.xlim([0,256])
	plt.show()

def colorWheelPlot(colorHist):
	# Plots color distribution on polar plot based on hue
	#
	# colorHist : histogram data for each hue value
	
	N = 360
	bottom = 4
	max_height = 4

	#normalize colorHist data
	maxVal = max(colorHist)
	colorHist = colorHist/float(maxVal)

	theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
	radii = max_height*colorHist
	width = (2*np.pi) / N

	ax = plt.subplot(111, polar=True)
	bars = ax.bar(theta, radii, width=width, bottom=bottom)
	plt.axis('off')

	i=0
	for r, bar in zip(radii, bars):
	    bar.set_facecolor(plt.cm.hsv(i))
	    i=i+1
	    bar.set_edgecolor('none')


	plt.show()

###########################################################################################
###########   DATA CREATION AND CONVERSION  ###############################################
###########################################################################################

def histValues(img):
	# Creates histogram array data for each channel and a total 
	#
	# img : image array (cv2.imread())

	histBlue = cv2.calcHist([img],[0],None,[256],[0,256])
	histGreen = cv2.calcHist([img],[1],None,[256],[0,256])
	histRed = cv2.calcHist([img],[2],None,[256],[0,256])
	histTotal = histBlue + histGreen + histRed

	return [histBlue, histGreen, histRed, histTotal]

def histToArray(hist):
	# Convets the hist data to an array. Needed for some numpy calculations
	#
	# hist : array of histogram array data
	# returns : array

	arr = []
	for item in hist:
		arr.append(item[0])
	return arr

def hsvData(img):
	# Creates HSV data from an image
	#
	# img : image array (cv2.imread*())

	#create copy of img to fill with hsv data
	hsvImg = img
	height, width, channels = img.shape

	for i in range(0,height):
		for j in range(0,width):
			#normalize r,g,b values for conversion function
			r = img[i,j,0] / float(255)
			g = img[i,j,1] / float(255)
			b = img[i,j,2] / float(255)

			h, s, v = colorsys.rgb_to_hsv(r,g,b)

			#unnormalize h,s,v values , round to nearest integer, and write to copied image
			hsvImg[i,j] = [int(round(h*360)) , int(round(s*100)) , int(round(v*100))]
		
	return hsvImg

###########################################################################################
###########   PREDICTION FUNCTIONS  #######################################################
###########################################################################################

def clipped(hist, totalPix):
	# Determines if there is whites or blacks are clipping
	#
	# hist : array of histogram array data
	# totalPix : total number of pixels times number of channels
	#
	# Checks clipping on first 10 pixels and last 10 pixels by checking 
	# if any of those pixels has a value above the threshold (limit) set to 
	# the average value for each pixel times 5

	limit = (totalPix/256) * 5
	if np.any(np.greater(hist[3][0:10], limit)):
		print("clipped blacks")

	if np.any(np.greater(hist[3][246:256], limit)):
		print("clipped whites")

def lifted(hist, totalPix):
	# Determines if there is lifted blacks
	#
	# hist : array of histogram array data
	# totalPix : total number of pixels times number of channels
	#
	# Checks to see if the average of the first 20 pixels is below a threshold 
	# value (limit) equal to the average of each bin divided by 30

	limit = totalPix/(256*30)
	if np.average(hist[3][0:20]) < limit:
		print("lifted blacks")

def crushed(hist):
	# Determines if there is crushed blacks
	#
	# hist : array of histogram array data
	#
	# Checks to see if there first half of slope data ever exceeds 11 times 
	# the average slope value. This is all calculated after absolute value has been
	# taken of slope data.


	arr = np.diff(histToArray(hist[3]))
	limit = np.average(np.absolute(arr))*11

	#[5:128] because there can sometimes be spike in first few pixels
	if np.any(np.greater(np.absolute(arr[5:128]), limit)):
		print("crushed blacks")
	

###########################################################################################
###########   MAIN PROGRAM  ###############################################################
###########################################################################################

def main():
	# read in image
	img = cv2.imread('colorTest.jpg')
	
	# create histogram data
	hist = histValues(img)


	# find image information
	height, width, channels = img.shape

	# determine total number of pixels, multiply by number of channels 
	#     multiply by number of channels because this is used to set threshold
	#     in fucntions using total data with is the total of all 3 channels
	totalPix = height * width * channels

	#plot histogram data
	#plotHist(hist)
	#plotDiff(hist)

	#plot color wheel
	hsvImg = hsvData(img)
	print(hsvImg)
	#determine if there is clipping or not
	clipped(hist, totalPix)

	#determine if there is lifted blacks or not
	lifted(hist, totalPix)

	#determine if there is crushed blacks or not
	crushed(hist)

	



main()


