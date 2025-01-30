# Discord bot: Youtube upload tracker

## Description
This program checks if a Youtube channel has uploaded a new video, by checking every 5 minutes against Google's API for new data. If a new video has been uploaded, then it automatically post a message on your Discord server. This is useful for promoting youtube channels to your audience in a discord server or following certain youtubers by receiving customizable notification alerts which can be viewed from your phone.

## Requirements
- Python installation and access to terminal
- Google Developer account
- Discord Developer account

- You will also need to create on this directory a new file called ".env", with the following keys for the program to work:

### .env
```
YOUTUBE_API_KEY= <Your_youtube_api_key_here>
YOUTUBE_CHANNEL_ID= <youtube_channel_you_want_to_track_here>
DISCORD_BOT_TOKEN=<token_for_your_discord_bot_here>
Discord_channel_id=<channel_in_your_discord_server_where_you_will_receive_the_video_update_notifications_here>
```

## Installation
```bash
git clone this repo
python -m venv test
```

| Windows                             | Linux/Mac                        |
|-------------------------------------|----------------------------------|
| `test\Scripts\activate`             | `source test/bin/activate`       |

```bash
pip install -r requirements.txt
python main.py
```
