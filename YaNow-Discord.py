from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from pypresence import Presence
import time, asyncio
from pypresence.exceptions import PipeClosed
import os

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
            print("The script was launched successfully (by y9chepux)")
            time.sleep(2)
            os.system('cls')
            print(" ")
            print("███ █  █ █▀▀ █▀▀█ █  █ ▀▄ ▄▀")
            print("█   █▀▀█ █▀▀ █  █ █  █   █  ")
            print("███ █  █ █▄▄ █▀▀▀ ▀▄▄▀ ▄▀ ▀▄")
            print(" ")
            print(" ")
            print("The code started without errors!")
            print("Support: https://t.me/y9chepux/")
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

buttons = [
    {
        "label": "Яндекс.Музыка",
        "url": "https://music.yandex.ru/"
    },
    {
        "label": "Developer",
        "url": "https://t.me/y9chepux/"
    }
]

media = ''
title = ''


run()

while True:
    try:
        try:
            if title != asyncio.run(get_media_info())["title"]:
                title = asyncio.run(get_media_info())["title"]
                media = asyncio.run(get_media_info())
                f = str(asyncio.run(get_player_info())).replace(".", " ").title()
                rpc.update(details=f'Слушает Яндекс Музыку', state=f'{media["artist"]} - {media["title"]}', large_image='yamusic-icon', large_text='UwU', buttons=buttons, start=time.time())
            else:
                time.sleep(1)
        except TypeError:
            rpc.clear()
            time.sleep(1)
    except PipeClosed:
        os.system("cls")
        print('[\033[38;05;196m•\033[m] Connection to Discord lost, restartning...')
        time.sleep(3)
        run()
