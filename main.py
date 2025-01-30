import discord
from discord.ext import tasks, commands
import googleapiclient.discovery
import os
import json
from save_load_files import save_dict_to_file, load_dict_lst_or_str__from_jsonfile
from dotenv import load_dotenv

# Replace these with your bot token and YouTube API key
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = int(os.getenv('Discord_channel_id'))  # Discord channel ID to post notifications
print('Channel_ID:', CHANNEL_ID) 

# YouTube channel details
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
YOUTUBE_CHANNEL_URL = f'https://www.youtube.com/channel/{YOUTUBE_CHANNEL_ID}'

# Initialize Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize YouTube API client
youtubeapi = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Store the last video ID to check for new uploads
last_video_dict = None
folder_path = "databases/"
JSON_NAME = folder_path+'YOUTUBEID_to_LASTVIDEOID.json'

if os.path.exists(JSON_NAME):
    last_video_dict = load_dict_lst_or_str__from_jsonfile(JSON_NAME)
    print(f'>Found pre-existing {JSON_NAME} + loaded successfully')
    print('Values found:', last_video_dict)
else:
    print(f'>Could not find {JSON_NAME}. Putting variable to empty dict')
    last_video_dict= {YOUTUBE_CHANNEL_ID: None}








@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    check_for_new_video.start()  # Start the task to check for new videos

@tasks.loop(minutes=5)  # Check every X minutes
async def check_for_new_video():
    global last_video_dict

    print('Starting Video checker Task')

    # Fetch the latest videos from the YouTube channel
    request = youtubeapi.search().list(
        part='snippet',
        channelId=YOUTUBE_CHANNEL_ID,
        maxResults=1,
        order='date'
    )
    response = request.execute()



    videos = response.get('items', [])

    
    pretty_json = json.dumps(response, indent=4)
    print('\nPretty Json:\n')
    print(pretty_json)


    pretty_json2 = json.dumps(videos, indent=4)
    print('\nVideo Found:\n')
    print(pretty_json2)



    if not videos: #no video found at all in the channel
        return

    latest_video = videos[0]
    latest_video_id = latest_video['id']['videoId']

    if last_video_dict[YOUTUBE_CHANNEL_ID] is None:
        # Store the ID of the latest video if we haven't checked before
        print('First time saving a video')
        last_video_dict[YOUTUBE_CHANNEL_ID] = latest_video_id
        save_dict_to_file(last_video_dict,JSON_NAME) #saved to json
        print('Saved to json')
        return

    elif latest_video_id != last_video_dict[YOUTUBE_CHANNEL_ID]:
        # A new video has been uploaded
        last_video_dict[YOUTUBE_CHANNEL_ID] = latest_video_id
        channelId = latest_video['snippet']['channelId']
        video_title = latest_video['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={latest_video_id}'
        channelTitle = latest_video['snippet']['channelTitle']
        video_description = latest_video['snippet']['description']
        publish_date = latest_video['snippet']['publishedAt']

        # Send a message to the Discord channel
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f'**{channelTitle}** uploaded a new video! **{video_title}**\n{video_url}') 
        save_dict_to_file(last_video_dict,JSON_NAME) #saved to json
        print('Saved to json')
    else:
        print('Channel has not uploaded a new video (when compared to previous saved latest video in json)')

bot.run(DISCORD_BOT_TOKEN)
