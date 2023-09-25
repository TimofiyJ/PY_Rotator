# import the necessary packages
import numpy as np
from skimage.transform import (hough_line, hough_line_peaks)
from matplotlib import pyplot as plt
import argparse
import cv2
import collections
from PIL import Image
from PIL import Image, ImageDraw


# construct the argument parse and parse the arguments
img_location = './invoices_rotated/images/lot.png'
output_file_path = "rotated_image.png"


my_image = cv2.imread(img_location, 0) #Fails if uses as-is due to bright background.
#Also try lines2 to see how it only picks up straight lines
#Invert images to show black background
image = ~my_image  #Invert the image (only if it had bright background that can confuse hough)

# Set a precision of 1 degree. (Divide into 180 data points)
# You can increase the number of points if needed. 
tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 180)

# Perform Hough Transformation to change x, y, to h, theta, dist space.
hspace, theta, dist = hough_line(image,tested_angles)

#Now, to find the location of peaks in the hough space we can use hough_line_peaks
h, q, d = hough_line_peaks(hspace, theta, dist)


#################################################################
#Example code from skimage documentation to plot the detected lines
angle_list=[]  #Create an empty list to capture all angles

# Generating figure 1
fig, axes = plt.subplots(1, 4, figsize=(15, 6))
ax = axes.ravel()

ax[0].imshow(image, cmap='gray')
ax[0].set_title('Input image')
ax[0].set_axis_off()

ax[1].imshow(np.log(1 + hspace),
             extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), dist[-1], dist[0]],
             cmap='gray', aspect=1/1.5)
ax[1].set_title('Hough transform')
ax[1].set_xlabel('Angles (degrees)')
ax[1].set_ylabel('Distance (pixels)')
ax[1].axis('image')

ax[2].imshow(image, cmap='gray')

origin = np.array((0, image.shape[1]))


for _, angle, dist in zip(*hough_line_peaks(hspace, theta, dist)):
    angle_list.append(angle) #Not for plotting but later calculation of angles
    y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
    ax[2].plot(origin, (y0, y1), '-r')
ax[2].set_xlim(origin)
ax[2].set_ylim((image.shape[0], 0))
ax[2].set_axis_off()
ax[2].set_title('Detected lines')

#Calculate mode 
mode_value = 0
mode_number = 0
angles = [((a*180/np.pi)+90)%360 for a in angle_list]

for i in list(set(angles)):
    if angles.count(i)>mode_value:
        mode_value = angles.count(i)
        mode_number = i

angle = mode_number
rotation = False
print(angle)
if angle>90 and angle<180:
    angle = 180-angle
    angle = -angle
    rotation = True

# if angle>90:
#     angle = angle-abs(90-angle)-90
# if angle<0:
#     angle = -angle

# if angle > 90:
#     angle = 180 - angle
#     if angle > 0:
#         angle = -angle
# elif angle>30:
#     angle = 90-angle
#     if angle>0:
#         angle = -angle

# else:
# 	if angle < -90:
# 		angle = abs(180-abs(angle))
# 	if angle < -30:
# 		angle = abs(90 - abs(angle))

# Calculate the image center
height, width = image.shape[:2]
center = (width // 2, height // 2)

# Create a rotation matrix
rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

width = 1980
height = 1040
# Apply the rotation to the image
#rotated_image = cv2.warpAffine(my_image, rotation_matrix, (width, height))
m_image = Image.open(img_location)
print(angle)
attitional_angle=0
if rotation==True:
    if angle>0:
        attitional_angle = 180
rotated_image = m_image.rotate(angle, expand=True, fillcolor="white")
rotated_image = rotated_image.rotate(attitional_angle, expand=True, fillcolor="white")

rotated_image.show()

ax[3].set_xlim(origin)
ax[3].set_axis_off()
ax[3].set_title('Result')
ax[3].set_ylim((my_image.shape[0], 0))

# Define the coordinates of the horizontal line (x1, y1, x2, y2)
x1, y1 = 0, 1050  # Replace with your desired coordinates
x2, y2 = m_image.width, 1050  # Replace with your desired coordinates

# Define the line color (in RGB format)
line_color = (255, 0, 0)  # Red color, you can change this
draw = ImageDraw.Draw(rotated_image)

# Draw the horizontal line
draw.line((x1, y1, x2, y2), fill=line_color, width=2)

ax[3].imshow(rotated_image)
plt.tight_layout()
plt.show()
#cv2.imshow("Rotated Image", rotated_image)
# Specify the file path to save the rotated image
# Save the rotated image to a local file
cv2.imwrite(output_file_path, rotated_image)
cv2.waitKey(0)

# ###############################################################
# # Convert angles from radians to degrees (1 rad = 180/pi degrees)
# angles = [a*180/np.pi for a in angle_list]

# # Compute difference between the two lines
# angle_difference = np.max(angles) - np.min(angles)
# print(180 - angle_difference)   #Subtracting from 180 to show it as the small angle between two lines
# cv2.waitKey(0)
