# import the necessary packages
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks)
from matplotlib import pyplot as plt
import argparse
import cv2
from PIL import Image
from PIL import Image, ImageDraw


# construct the argument parse and parse the arguments
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
ap.add_argument("-o", "--output", required=True,
	help="path to output image file")

args = vars(ap.parse_args())

# get the arguments
img_location = str(args["image"])
output_file_path = str((args["output"]))
my_image = cv2.imread(img_location)

#Invert images to show black background
image = ~my_image

# Set a precision of 1 degree. (Divide into 180 data points)
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180)

# Perform Hough Transformation to change x, y, to h, theta, dist space.
hspace, theta, dist = hough_line(image,tested_angles)

#Now, to find the location of peaks in the hough space we can use hough_line_peaks
h, q, d = hough_line_peaks(hspace, theta, dist)

angle_list=[]  #Create an empty list to capture all angles

# SHOWING THE COMPUTATIONS BETWEEN INPUT AND RESULT
# Generating figure 1
# fig, axes = plt.subplots(1, 4, figsize=(15, 6))
# ax = axes.ravel()

# ax[0].imshow(image, cmap='gray')
# ax[0].set_title('Input image')
# ax[0].set_axis_off()

# ax[1].imshow(np.log(1 + hspace),
#              extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), dist[-1], dist[0]],
#              cmap='gray', aspect=1/1.5)
# ax[1].set_title('Hough transform')
# ax[1].set_xlabel('Angles (degrees)')
# ax[1].set_ylabel('Distance (pixels)')
# ax[1].axis('image')

# ax[2].imshow(image, cmap='gray')

# origin = np.array((0, image.shape[1]))


# for _, angle, dist in zip(*hough_line_peaks(hspace, theta, dist)):
#     angle_list.append(angle) #Not for plotting but later calculation of angles
#     y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
#     ax[2].plot(origin, (y0, y1), '-r')
# ax[2].set_xlim(origin)
# ax[2].set_ylim((image.shape[0], 0))
# ax[2].set_axis_off()
# ax[2].set_title('Detected lines')

#Calculate mode(most common angle = angle of the lines in our picture)

mode_value = 0
mode_number = 0
angles = [((a*180/np.pi)+90)%360 for a in angle_list]

for i in list(set(angles)):
    if angles.count(i)>mode_value:
        mode_value = angles.count(i)
        mode_number = i

angle = mode_number
rotation = False
if angle>90 and angle<180:
    angle = 180-angle
    angle = -angle
    rotation = True

# Calculate the image center
height, width = image.shape[:2]
center = (width // 2, height // 2)

# Create a rotation matrix
rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

width = 1980
height = 1040

# Apply the rotation to the image
m_image = Image.open(img_location)

#calculating additional angle if needed(if angle was>90)
attitional_angle=0
if rotation==True:
    if angle>0:
        attitional_angle = 180

rotated_image = m_image.rotate(angle, expand=True, fillcolor="white")
rotated_image = rotated_image.rotate(attitional_angle, expand=True, fillcolor="white")

rotated_image.show()

#SHOWING THE FINAL RESULT
# ax[3].set_xlim(origin)
# ax[3].set_axis_off()
# ax[3].set_title('Result')
# ax[3].set_ylim((my_image.shape[0], 0))
# ax[3].imshow(rotated_image)
# plt.tight_layout()
# plt.show()

# Save the rotated image to a local file
cv2.imwrite(output_file_path, rotated_image)
print("Press any key to exit")
end = input()
