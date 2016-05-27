from telegram.ext import Updater, StringCommandHandler, StringRegexHandler, MessageHandler, CommandHandler, RegexHandler, Filters
from telegram.ext.dispatcher import run_async
import telegram
import yaml
import json
import os.path
import logging
from groupinfo import GroupInfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DATA_FILENAME = 'data.dat'
START_TEXT = ''
# In the interest of full disclosure
PRIVACY_TEXT = '*Privacy Information*\n\nIn order for this bot to work, we require access to all messages sent in your groups. As a result we provide this privacy information to let you know what we do with your data.\n\n\
Messages sent in your group(s) are processed by the bot to build a unique Markov chain, which is used to automatically generate sentences. \
This stores your messages in a combined form - they are never stored or outputted in full. When many messages are combined in this way it becomes \
difficult to reconstruct the original sentences, but it may still be possible to relate the data back to you. This data is never shared with any third parties.\n\n\
Please do not invite this bot to channels where sensitive or private topics are discussed. This bot carries no warranty, express or implied, and the owners/maintainers/\
providers of this bot take no responsibility for any consequences that may arise from its use in any way.'

groups = {}


def start(bot, update):
    bot.send_message(update.message.chat_id, text=START_TEXT)

def privacy(bot, update):
    bot.send_message(update.message.chat_id, text=PRIVACY_TEXT, parse_mode=telegram.ParseMode.MARKDOWN)

def message(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text

    global groups
    if chat_id not in groups:
        groups[chat_id] = GroupInfo(chat_id)

    groups[chat_id].add_message(message)
    pass

def main():
    # Load telegram API stuff
    settings = open('config.yml', 'r')
    yaml_data = yaml.load(settings)
    token = yaml_data['telegram-apikey']
    updater = Updater(token, workers=10)

    # Load saved data
    global groups
    if os.path.isfile(DATA_FILENAME):
        try:
            with open(DATA_FILENAME, 'r') as saved:
                data = json.loads(saved.read())
                for chat_id in data:
                    groups[chat_id] = GroupInfo(chat_id, data[chat_id])
        except ValueError:
            logging.info("No JSON saved data found")

    # Register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler([Filters.text], message))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("privacy", privacy))

    updater.start_polling(timeout=10)

    logging.info("Bot started!")

    # CLI
    while True:
        try:
            text = raw_input()
        except NameError:
            text = input()

        if text == 'stop':
            logging.info("Saving all data...")
            save_data = {}
            for chat_id in groups:
                save_data[chat_id] = groups[chat_id].get_data()

            with open(DATA_FILENAME, 'w') as save_file:
                json.dump(save_data, save_file)

            logging.info("Saved, stopping.")

            updater.stop()
            break

if __name__ == '__main__':
    main()
