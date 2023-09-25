# import the necessary packages
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
args = vars(ap.parse_args())
# load the image from disk
image = cv2.imread(args["image"])

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
# Extract x and y values from the points
x_values = [point[1] for point in coords]
y_values = [point[0] for point in coords]


# Create a scatter plot
plt.scatter(x_values, y_values, label='Points', color='blue', marker='o')

# Add labels and a legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot of Points')
plt.legend()

# Show the plot
plt.imshow(image)
plt.show()
print(coords)

# most_left_pixel = coords[]

# angle = cv2.minAreaRect(coords)[-1]
# # Convert the rectangle's parameters to integers

# rect = cv2.minAreaRect(coords)
# print(rect)

# # Calculate the vertices of the rotated rectangle
# box = cv2.boxPoints(((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), angle))
# box = np.int0(box)


# # the `cv2.minAreaRect` function returns values in the
# # range [-90, 0); as the rectangle rotates clockwise the
# # returned angle trends to 0 -- in this special case we
# # need to add 90 degrees to the angle
# if angle > 30:
# 	angle = abs(90 - angle)
# # otherwise, just take the inverse of the angle to make
# # it positive
# else:
# 	angle = -angle

	
# # rotate the image to deskew it
# (h, w) = image.shape[:2]
# center = (w // 2, h // 2)
# M = cv2.getRotationMatrix2D(center, angle, 1.0)
# rotated = cv2.warpAffine(image, M, (w, h),
# 	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# # draw the correction angle on the image so we can validate it
# cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
# 	(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
# # show the output image
# print("[INFO] angle: {:.3f}".format(angle))

# # Use cv2.resize() to resize the image

# cv2.imshow("Input", image)
# cv2.imshow("Rotated",rotated)

# cv2.drawContours(gray, [box], 0, (255, 255, 255), 2)
# cv2.imshow("Gray", gray)

# cv2.waitKey(0)
