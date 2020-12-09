import pydub
import bot_utils
import config
import bot_utils
import telebot




bot = telebot.TeleBot(config.TOKEN, threaded=False)

@bot.message_handler(content_types=["audio"])
def download_music_file(message):

     #         reading file from TG server
     file_link=bot.get_file(message.audio.file_id).file_path
     url=config.SERVER_FILES_DIR+file_link
     print("got url")
     local_name=config.LOCAL_MP3_DIR + bot_utils.cut_path(file_link)
     with open(url, "rb") as f:
          data=f.read()
     with open("something.mp3", "wb") as t:
          t.write(data)
     f.close()
     t.close()

if __name__ == '__main__':
     bot.infinity_polling()
