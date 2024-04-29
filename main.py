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


@bot.on_callback_query()
async def callbackquery(client:Client, callbackquery: CallbackQuery):
    user_id =callbackquery.from_user.id
    data = callbackquery.data


    if data == "audio":
        # Delete message past
        await callbackquery.message.delete()
        sent_message = await callbackquery.message.reply_text(
        text="⏳ Processing...",
        )
        youtube_audio= youtube.streams.get_by_itag(140)
        youtube_audio.download(DOWNLOAD_LOCATION)
        file_name = youtube.streams.get_by_itag(140).default_filename
        file_dir = f"{DOWNLOAD_LOCATION}{file_name}"
        # Send audio to user
        await sent_message.edit(
            text="📤 Sending..."
        )
        await callbackquery.message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await client.send_audio(
            chat_id=user_id,
            audio=open(file_dir, "rb"),
            caption="💫download by:\nYoutubed-Downloader-Bot",
            file_name=file_name
        )
        await sent_message.delete()
        # Delete video from disk after sending to user
        os.remove(file_dir)


    elif data == "360":
        # Delete message past
        await callbackquery.message.delete()
        sent_message = await callbackquery.message.reply_text(
        text="⏳ Processing...",
        )
        youtube_stream = youtube.streams.get_by_itag(18)
        youtube_stream.download(DOWNLOAD_LOCATION)
        file_name = youtube.streams.get_by_itag(18).default_filename
        file_dir = f"{DOWNLOAD_LOCATION}{file_name}"
        # Send video to user
        await sent_message.edit(
            text="📤 Sending..."
        )
        await callbackquery.message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
        await client.send_video(
            chat_id=user_id,
            video=open(file_dir, "rb"),
            caption="💫download by:\nYoutubed-Downloader-Bot",
            file_name=file_name
        )
        await sent_message.delete()
        # Delete video from disk after sending to user
        os.remove(file_dir)

        
    elif data == "720":
        # Delete message past
        await callbackquery.message.delete()
        sent_message = await callbackquery.message.reply_text(
        text="⏳ Processing...",
        )
        youtube_stream = youtube.streams.get_by_itag(22)
        youtube_stream.download(DOWNLOAD_LOCATION)
        file_name = youtube.streams.get_by_itag(22).default_filename
        file_dir = f"{DOWNLOAD_LOCATION}{file_name}"
        # Send video to user
        await sent_message.edit(
            text="📤 Sending..."
        )
        await callbackquery.message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
        await client.send_video(
            chat_id=user_id,
            video=open(file_dir, "rb"),
            caption="💫download by:\nYoutubed-Downloader-Bot",
            file_name=file_name
        )
        await sent_message.delete()
        # Delete video from disk after sending to user
        os.remove(file_dir)