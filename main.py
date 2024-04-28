from pyrogram import Client,filters,enums
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pytube import YouTube
import os, re


# Enter the bot information
bot = Client(
    "Youtubed-Downloader-Bot",
    api_id="ENTER YOUR API ID",
    api_hash="ENTER YOUR API HASH",
    bot_token="ENTER YOUR BOT TOKEN",
)


# Download location variables
DOWNLOAD_LOCATION = "./temp/"


# Send welcome message to new users
@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text('Welcome to my youtube downloader bot.\nSend me your video link to download')


# Download video from youtube and send to user
@bot.on_message()
async def download(client: Client, message: Message):
    # Getting chat id user
    user_id = message.from_user.id
    # Getting link video user
    link = message.text
    # Check if user message is a valid youtube video link
    pattern = r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    result = re.match(pattern, link)
    if result:
        # Create an object
        global youtube
        youtube = YouTube(link)
        # Getting user link information
        channel = youtube.author
        titel = youtube.title
        views = youtube.views
        publish_date = youtube.publish_date
        publish_date = str(publish_date).split()
        length = youtube.length
        # Getting the volume
        res360p_and_res720 = ""
        audio = ""
        streams = youtube.streams.filter(file_extension="mp4")
        # videos
        for stream in streams:
            if stream.resolution in ["360p", "720p"] and stream.is_progressive:
                res360p_and_res720 += f" 🎬  {stream.resolution} - {stream.filesize / (1024 * 1024):.1f} MB\n"
        # audio
        for stream in youtube.streams.filter(abr="128kbps"):
            audio += f" 🎵 audio - {stream.filesize / (1024 * 1024):.2f} MB"
        # String information link video
        text = f"""
channel: {channel}
{titel}
views: {f"{int(views):,}"}
time:second {length}
publish date: {publish_date[0]}
{res360p_and_res720[:-1]}
{audio}
        """
        # Buttons
        markup = InlineKeyboardMarkup([
            [
            InlineKeyboardButton(text="360p",callback_data="360"),
            InlineKeyboardButton(text="720p",callback_data="720"),
            InlineKeyboardButton(text="audio", callback_data="audio")  
            ]
        ])
        # Getting to image link
        img = youtube.thumbnail_url
        # Send message for user
        await client.send_photo(
            chat_id=user_id,
            photo=img,
            caption=text,
            reply_markup=markup
        )
    else:
        # Send message for user 
        await message.reply_text("❌ The link is wrong!.. try another link.")