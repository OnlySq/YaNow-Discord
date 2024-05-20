from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from pypresence import Presence
import time, asyncio
from pypresence.exceptions import PipeClosed
import os
from urllib.parse import quote
from datetime import datetime, timezone

THUMBNAIL_BUFFER_SIZE = 5 * 1024 * 1024
CID = '1221371159510253598'

rpc = Presence(CID)

def run():
    while True:
        try:
            rpc.connect()
            os.system("cls")
            print('[\033[01;38;05;46m•\033[m] Connected to Discord')
            time.sleep(2)
            os.system('cls')
            print(" ")
            print("███ █  █ █▀▀ █▀▀█ █  █ ▀▄ ▄▀")
            print("█   █▀▀█ █▀▀ █  █ █  █   █  ")
            print("███ █  █ █▄▄ █▀▀▀ ▀▄▄▀ ▄▀ ▀▄")
            print(" ")
            print(" ")
            print("Program version: 1.3.0")
            print("Program site: https://chepux.wixsite.com/yanow-for-discord/")
            print("Support: https://t.me/chepuxcat/")
            break
        except:
            os.system("cls")
            print('[\033[38;05;226m•\033[m] Waiting discord running to connect...')
            time.sleep(10)
            continue

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])
        return info_dict

async def get_time_info() -> str:
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = current_session.get_timeline_properties()
        return info.end_time

async def get_player_info() -> str:
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        id = current_session.source_app_user_model_id
        return str(id)

media = ''
title = ''

run()

while True:
    try:
        try:
            new_title = asyncio.run(get_media_info())["title"]
            if title != new_title:
                title = new_title
                media = asyncio.run(get_media_info())
                f = str(asyncio.run(get_player_info())).replace(".", " ").title()
                artist_encoded = quote(media["artist"])
                title_encoded = quote(media["title"])
                buttons = [
                    {
                        "label": "Яндекс.Музыка",
                        "url": f"https://music.yandex.ru/search?text={artist_encoded}%20{title_encoded}&type=tracks"
                    },
                    {
                        "label": "Program website",
                        "url": "https://chepux.wixsite.com/yanow-for-discord/"
                    }
                ]
                start_time = datetime.now(timezone.utc).timestamp()
                rpc.update(details='Слушает Яндекс Музыку', state=f'{media["artist"]} - {media["title"]}', large_image='yamusic-orig', large_text='Яндекс.Музыка', buttons=buttons, start=start_time)
            else:
                time.sleep(1)
        except TypeError:
            rpc.clear()
            time.sleep(1)
    except PipeClosed:
        os.system("cls")
        print('[\033[38;05;196m•\033[m] Connection to Discord lost, restarting...')
        time.sleep(3)
        run()
