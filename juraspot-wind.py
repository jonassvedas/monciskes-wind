import requests
import pytesseract
# import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

avg_wind_url = "http://juraspot.lt/images/10MinAvgWindSpeed.php"
dir_wind_url = "http://juraspot.lt/images/WindDirection.php"

avg_wind_img = "avg_wind.png"
dir_wind_img = "dir_wind.png"

img = requests.get(avg_wind_url).content
with open(avg_wind_img, 'wb') as handler:
    handler.write(img)

img = requests.get(dir_wind_url).content
with open(dir_wind_img, 'wb') as handler:
    handler.write(img)

# process wind speed
speed_data = pytesseract.image_to_string(Image.open(avg_wind_img)).split()
speed = speed_data[5]
date = speed_data[6]
time = speed_data[7]

# process wind direction
img = Image.open(dir_wind_img).convert('RGB')

img_data = np.array(img)

# Extract red pixels first then check which ones are not equal to 0 for color red
img_x = img_data.shape[0]
img_y = img_data.shape[1]

center = np.array([img_y/2, img_x/2])

r = img_data[:,:,0] == 255
g = img_data[:,:,1] == 0
b = img_data[:,:,2] == 0
red_pixels = r * g * b

red_coordinates = np.argwhere(red_pixels == True)
red_avg = np.mean(red_coordinates, axis = 0)

# Normalize and invese y axis
norm = (center - red_avg) * np.array([1,-1])

angle = int(np.arctan2(norm[0], norm[1]) / 3.1416 * 180)

# plt.imshow(red_pixels)
# plt.show()

print(angle, "deg |", speed, "m/s |", date, time)