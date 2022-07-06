# monciskes-wind

## About
This is a script that sends a telegram notification via a bot to notify users when wind is good for kiteboarding in Monciskes.
Data is taken from the wind station provided by juraspot.lt.

Wind is checked every 30 minutes and a notification is sent when:
* wind speed is between 6.5 and 13.5 m/s
* wind direction is on-shore (180°-0°)
* the sun is up :)

## How to install
Download and install Telegram messaging app on your device:
https://telegram.org/

In the search field type `monciskes-wind` to find the bot and start a conversation.
Click `START` in the conversation window to enable the bot.

Or you can simply find the bot clicking on the following link and following the instructions: https://t.me/monciskes_wind_bot

## For developers

### How to test
To avoid sending messages to all users during testing a test mode is available
via the -q option.

### Dependencies

Tesseract:
https://tesseract-ocr.github.io/

Python Packages:
- requests
- Pillow
- numpy
- pytesseract
- suntime
- pytz
