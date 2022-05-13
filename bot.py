import config
import parser
import telebot
import time
import threading

from parser import get_meetings
bot = telebot.TeleBot(config.token)

chat_ids = set()


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Starting...')
        chat_ids.add(message.chat.id)


wait_timer = 10


def parse_meeting(meeting):
    place = int(meeting['places'].split(" ")[0])
    print(meeting['date'], " have ", place, "places")
    if place >= 1:
        return True
    return False


def send_messages():
    global prev_meetings
    t = time.time()
    while(True):
        if(time.time() - t > wait_timer):
            meetings = get_meetings()
            text = ""
            for meeting in meetings:
                is_have_places = parse_meeting(meeting)
                if is_have_places:
                    text += meeting['date'] + ": " + meeting['places'] + '\n'
                    for chat_id in chat_ids:
                        bot.send_message(chat_id, text)
            t = time.time()


if __name__ == '__main__':
    t = threading.Thread(target=send_messages)
    t.start()

    while(True):
        bot.infinity_polling()
