#! python3
from notify import *
import requests
import pytesseract
import argparse
from PIL import Image
import numpy as np
from math import acos, sqrt, pi
from suntime import Sun
import pytz
from datetime import datetime

raw_data_file= "raw_data.csv"

avg_wind_url = "http://juraspot.lt/images/10MinAvgWindSpeed.php"
dir_wind_url = "http://juraspot.lt/images/WindDirection.php"

avg_wind_img = "avg_wind.png"
dir_wind_img = "dir_wind.png"

wind_min, wind_max = (6.5, 13.5)
# for the angle settings North is assumed at 0 degrees, angle is increasing clockwise.
# angle is from 0 to 359
dir_start, dir_end = (180, 0)
latitude, longitude = (56.005, 21.076)

def is_angle_ok(angle, start, end):
    if start <= end:
        if (angle >= start) and (angle <= end):
            return True
    else:
        if not((angle >= end) and (angle <= start)):
            return True
    return False

def is_speed_ok(speed, min_speed, max_speed):
    if (speed >= min_speed) and (speed <= max_speed):
        return True
    else:
        return False

def get_time():
    return pytz.utc.localize(datetime.utcnow())

def is_sunlight_ok(time):
    sun = Sun(latitude, longitude)
    sunrise = sun.get_sunrise_time()
    sunset = sun.get_sunset_time()

    if (sunrise < time < sunset):
        return True
    return False


def download_img_from_url(url, dest):
    img = requests.get(url).content
    with open(dest, 'wb') as handler:
        handler.write(img)

def get_wind_speed(url):
    download_img_from_url(url, avg_wind_img)

    img = Image.open(avg_wind_img).convert('RGB')
    # process wind speed
    speed_data = pytesseract.image_to_string(img, config='tessedit_char_whitelist=0123456789.').split()

    img_data = np.array(img)
    r = img_data[:,:,0] == 0
    g = img_data[:,:,1] == 0
    b = img_data[:,:,2] == 255
    blue_pixels = r * g * b
    count = np.sum(blue_pixels)

    speed = float(speed_data[5])
    # Hack for tesseract bug of detecting 7 as 1
    if count > 1000 and int(speed) == 1:
        speed = speed + 6

    date = speed_data[6]
    time = speed_data[7]

    return (speed, date, time)

def angle_to_direction(angle):
    if 0 < angle <= 11.25:
        return "N"
    elif 11.25 < angle <= 33.75:
        return "NNE"
    elif 33.75 < angle <= 56.25:
        return "NE"
    elif 56.25 < angle <= 78.75:
        return "ENE"
    elif 78.75 < angle <= 101.25:
        return "E"
    elif 101.25 < angle <= 123.75:
        return "ESE"
    elif 123.75 < angle <= 146.25:
        return "SE"
    elif 146.25 < angle <= 168.75:
        return "SSE"
    elif 168.75 < angle <= 191.25:
        return "S"
    elif 191.25 < angle <= 213.75:
        return "SSW"
    elif 213.75 < angle <= 236.25:
        return "SW"
    elif 236.25 < angle <= 258.75:
        return "WSW"
    elif 258.75 < angle <= 281.25:
        return "W"
    elif 281.25 < angle <= 303.75:
        return "WNW"
    elif 303.75 < angle <= 326.25:
        return "NW"
    elif 326.25 < angle <= 348.75:
        return "NNW"
    elif 348.75 < angle < 360:
        return "N"

def get_wind_angle(url):
    download_img_from_url(url, dir_wind_img)

    # process wind direction
    img = Image.open(dir_wind_img).convert('RGB')
    img_data = np.array(img)

    # Extract red pixels first then check which ones are not equal to 0 for color red
    img_x = img_data.shape[0]
    img_y = img_data.shape[1]

    # Offset compass center by 3 pixels up due to inaccurate image.
    center = np.array([img_y/2 - 3, img_x/2])

    r = img_data[:,:,0] == 255
    g = img_data[:,:,1] == 0
    b = img_data[:,:,2] == 0
    red_pixels = r * g * b

    red_coordinates = np.argwhere(red_pixels == True)
    red_avg = np.mean(red_coordinates, axis = 0)

    # Normalize and invese y axis
    norm = (red_avg - center) * np.array([-1, 1])

    x = norm[1]
    y = norm[0]

    # get angle between wind directiona and vector at (0,1) (north)
    try:
        angle = int(acos(y/sqrt(x**2+y**2)) / (2*pi) * 360)
        angle = angle if x >= 0 else 360 - angle
    except ZeroDivisionError:
        angle = 0

    # Debug
    #print("Red pixels avg: ",red_avg)
    #print("angle: ", angle)
    #import matplotlib.pyplot as plt
    #plt.imshow(red_pixels)
    #plt.plot(center[1],center[0],'.')
    #plt.plot(red_avg[1],red_avg[0],'.')
    #plt.show()

    return angle

def save_raw_data(filename, data_string):
    f = open(filename, "a")
    f.write(data_string)
    f.close()

def main(args):

    speed, date, time = get_wind_speed(avg_wind_url)
    angle = get_wind_angle(dir_wind_url)
    direction = angle_to_direction(angle)

    text = "Monciškės: {}m/s | {} ({}°) ".format(speed, direction, angle)

    time = get_time()
    angle_ok = is_angle_ok(angle, dir_start, dir_end)
    speed_ok = is_speed_ok(speed, wind_min, wind_max)
    sunlight_ok = is_sunlight_ok(time)

    print(text)
    print("Angle OK: {}, Speed OK: {}, Sunlight OK: {}".format(angle_ok, speed_ok, sunlight_ok))

    csv_format = time.strftime("%Y-%m-%d, %H:%M:%S, ") + str(speed) + ", " + str(angle) + "\n"
    save_raw_data(raw_data_file, csv_format)

    if (angle_ok and speed_ok and sunlight_ok):
        ids = get_chat_ids(args.bot_api_key)
        save_chat_ids_to_db(ids)
        if not args.quiet:
            send_telegram(args.bot_api_key, text, ids)
    else:
        ids = get_chat_ids(args.bot_api_key)
        save_chat_ids_to_db(ids)


def get_args():
    usage = '\nThis program will send a telegram notification if wind conditions for kiteboarding are good in Monciskes.\n'
    parser = argparse.ArgumentParser(
            usage=usage,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-b','--bot-api-key', type = str,
                        required = True,
                        help = 'Telegram bot API key.')

    parser.add_argument('-q','--quiet', action='store_true',
                        help = 'Runs quietly without sending an update.')

    args, unparsed = parser.parse_known_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
