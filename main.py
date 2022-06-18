import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from trascrypt import Transcryptor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Bot:
  def __init__(self):
    self.updater = None
    self.dispatcher = None
    self.handlers = []
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    model_name = os.getenv('MODEL_NAME')
    self.app = ApplicationBuilder().token(token).build()
    self.transcryptor = Transcryptor(model_name)

  async def get_voice(self, update: Update, context) -> None:
    # get basic info about the voice note file and prepare it for downloading
    new_file = await context.bot.get_file(update.message.voice.file_id)
    # download the voice note as a file
    await new_file.download(f"voice_note.ogg")
    # transcrypt the voice note
    transcrypted_text = self.transcryptor.transcrypt("voice_note.ogg")
    # send the transcrypted text to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=transcrypted_text)

  async def get_video(self, update: Update, context) -> None:
    # get basic info about the voice note file and prepare it for downloading
    new_file = await context.bot.get_file(update.message.video_note.file_id)
    # download the voice note as a file
    await new_file.download(f"video_note.mp4")
    # transcrypt the voice note
    transcrypted_text = self.transcryptor.transcrypt("video_note.mp4")
    # send the transcrypted text to the user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=transcrypted_text)

  def start(self):
    self.app.add_handler(MessageHandler(filters.VOICE, self.get_voice))
    self.app.add_handler(MessageHandler(filters.VIDEO_NOTE, self.get_video))
    self.app.run_polling()


if __name__ == '__main__':
  bot = Bot()
  bot.start()
