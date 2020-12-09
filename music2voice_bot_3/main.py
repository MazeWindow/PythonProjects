import telebot
import config
import bot_utils
import os

bot = telebot.TeleBot(config.TOKEN, threaded=False)
music_file=""


@bot.message_handler(content_types=["audio"])
def download_music_file(message):
     global music_file

     print("Messaging:", message.from_user)

     file_link = bot.get_file(message.audio.file_id).file_path  # getting file directory in bots "files/" dir
     music_file = bot_utils.cut_path(file_link)  # storing file name in global variable for use from within
     bot_utils.tg_download_music(file_link) # downloading file from TG server

     # passing action further
     bot.send_message(message.chat.id, "Cool! Now send me timecodes", reply_to_message_id=message.message_id)
     bot.register_next_step_handler(message, process_audio)


def initiate_cutting_sequecne():
     pass



def process_audio(message):
     global music_file
     timecodes_string=message.text
     print("getting timings...", end=" ")
     timing_start, timing_end=bot_utils.get_timecodes(timecodes_string)
     print("timings recieved")
     print("launching converter...", end=" ")
     opus_name=bot_utils.convert_sound(timing_start, timing_end, music_file)
     print("converter returned")
     with open(opus_name, "rb") as f:
          voice_file=f.read()
     bot.send_voice(message.chat.id, voice_file, None)
     print("    deleting ogg:", config.LOCAL_MP3_DIR + music_file)
     os.remove(config.LOCAL_MP3_DIR + music_file)
     print("    deleted successfully")
     return


@bot.message_handler(commands=["again"])
def greetings(message):
     msg=message.reply_to_message
     if not msg.audio:
          bot.send_message(message.chat.id, "I don't see any music here", reply_to_message_id=msg.message_id)
     else:
          pass


@bot.message_handler(commands=["start"])
def greetings(message):
     current_chat_id=message.chat.id
     bot.delete_message(message.chat.id, message.message_id)
     greetings_text="Hello! I am cut'n'voice bot\n" \
                    "I convert music into a voice messages\n" \
                    "Use /help to get instructions"
     bot.send_message(current_chat_id, greetings_text)

@bot.message_handler(commands=["help"])
def instructor(message):
     bot.send_message(message.chat.id, "under construction")
     pass

if __name__ == '__main__':
     bot.infinity_polling()
