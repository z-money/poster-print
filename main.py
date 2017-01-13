import cv2
import numpy as np
import datetime

from subprocess import Popen, PIPE

def subp_run(cmd):
	p = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
	return p.communicate()[0].decode('UTF-8').strip()

cv2.namedWindow('test')
vc = cv2.VideoCapture(0)

n = 8    # Number of levels of quantization

indices = np.arange(0,256)   # List of all colors 

divider = np.linspace(0,255,n+1)[1] # we get a divider

quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors

color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..

palette = quantiz[color_levels] # Creating the palette


if vc.isOpened():
	rval, frame = vc.read()
else:
	rval = False

height = frame.shape[0]
width = frame.shape[1]

frozen = False

switch = 2

while rval:
	if(frozen != True):
		sm_frame = frame[:,width/4:3*width/4]
		if(switch == 1):
			im = cv2.cvtColor(sm_frame, cv2.COLOR_RGB2GRAY)
		elif(switch == 2):
			im = palette[sm_frame]  # Applying palette on image
			im = cv2.convertScaleAbs(im)
			im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
		# im = palette[frame]  # Applying palette on image
		# im = cv2.convertScaleAbs(im)
		# cv2.rectangle(frame, (width/4,0), (3*width/4,height), (0,255,0), 2)
		cv2.imshow('test', im)
		
		rval, frame = vc.read()
		key = cv2.waitKey(50)
		if(key == 27):
			break
		elif(key == 49):
			switch = 1
		elif(key == 50):
			switch = 2
		elif(key == 32):
			frozen = True
	elif(frozen):
		cv2.imshow('test', im)
		rval, frame = vc.read()
		key = cv2.waitKey(50)
		if(key == 27):
			break
		elif(key == 32):
			stamp = datetime.datetime.now()
			cv2.imwrite('images/portrait_%s.png' % stamp, im)
			# subp_run('lp -o portrait -o fit-to-page -o media=Letter images/portrait_%s.png' % stamp)
			frozen = False
		elif(key == 27):
			frozen = False
cv2.destroyWindow('test')





