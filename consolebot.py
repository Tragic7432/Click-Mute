from g_python.g_python_bot import ChatBot
from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage
from g_python.hpacket import HPacket
from g_python.htools import RoomUsers
from time import sleep

extension_info = {
    "title": "ConsoleBot",
    "description": "click mute with consolebot",
    "version": "1.0",
    "author": "Toxicwave"
}

def show_them(users):
    for user in users:
        user_list.update({user.id: user.name})

ext = Extension(extension_info, args=['-p', '9092'])
ext.start()
room_users = RoomUsers(ext)
room_users.on_new_users(show_them)
user_list = dict()

current_value = ''

room_id = ''


def kick_user(message: HMessage):
    global room_id
    user_id = message.packet.read_int()
    nickname = str()
    for id in user_list:
        if id == user_id:
            nickname = user_list[id]
    if current_value == True:
        ext.send_to_client(HPacket('Whisper', -1, nickname + "  Muted", 0, 30, 0, -1))
        ext.send_to_server(HPacket('MuteUser', user_id, room_id, 99999))



def start():
 global current_value
 current_value = True
 console_bot.send_message("Click-mute is enabled.")
 sleep(1)
 console_bot.send_message("Please rejoin to your current room if you havent.")

def stop():
    global current_value
    current_value = False
    console_bot.send_message("Click-mute is disabled.")

def exit():
    console_bot.hide_bot()

def roomsearch(message):
    global room_id
    roomad = message.packet.read_int()
    room_id = roomad



ext.intercept(Direction.TO_SERVER, kick_user, 'GetSelectedBadges')
ext.intercept(Direction.TO_CLIENT, roomsearch, 'OpenConnection')

console_bot = ChatBot(ext, botname="toxicwave")
console_bot.on_command(':exit', exit)
console_bot.on_command(':stop', stop)
console_bot.on_command(':start', start)
console_bot.start()
console_bot.send_message("Welcome! Use :start or :stop")
