# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
ap.add_argument("-o", "--output", required=True,
	help="path to output image file")

args = vars(ap.parse_args())

# get the arguments
image = cv2.imread(args["image"])
output = str((args["output"]))

if output == None:
	output = "./output.png"

# convert the image to grayscale and flip the foreground
# and background to ensure foreground is now "white" and
# the background is "black"

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)

# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0

thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates

coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]

#making additional calculations for the correct angle
if angle > 30:
	angle = abs(90 - angle)
else:
	angle = -angle
	
# rotate the image to deskew it
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# show the degrees
print("[INFO] angle: {:.3f}".format(angle))

cv2.imwrite(output,rotated)
print("Press any key to exit")
end = input()