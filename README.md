# monciskes-wind

## About
This is a script that sends a Telegram notification via the
[`@monciskes_wind_bot`](https://t.me/monciskes_wind_bot) bot and to the
[`@monciskeswind`](https://t.me/monciskeswind) channel when wind is good for
kiteboarding in Monciskes.
Data is taken from the wind station provided by juraspot.lt.

Wind is checked every 30 minutes and a notification is sent when:
* wind speed is at least 6 m/s
* wind direction is on-shore (180°-0°)
* the sun is up :)

## How to install
Join the [`@monciskeswind`](https://t.me/monciskeswind) channel in Telegram,
or start a conversation with [`@monciskes_wind_bot`](https://t.me/monciskes_wind_bot).

## For developers

### How to test
To avoid sending messages to all users during testing a test mode is available
via the -q option.

### Running

Add the bot to the channel as an administrator with permission to post
messages, then set its token without placing it on the command line:

```bash
export TELEGRAM_BOT_TOKEN='your-token'
./run.sh
```

`run.sh` sends a real channel message when conditions are suitable. Use `-q`
directly with `monciskes-wind.py` to test without sending a message.

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
