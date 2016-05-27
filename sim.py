from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
import telegram
import yaml
import json
import ast
import os.path
import logging
from groupinfo import GroupInfo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DATA_FILENAME = 'data.dat'
START_TEXT = 'This bot constructs sentences based off your group\'s previous messages. Invite it to your group and try it out with /generate. You may have to wait for enough messages to be gathered \
to get good messages'
# In the interest of full disclosure
PRIVACY_TEXT = '*Privacy Information*\n\nIn order for this bot to work, we require access to all messages sent in your groups. As a result we provide this privacy information to let you know what we do with your data.\n\n\
Messages sent in your group(s) are processed by the bot to build a unique Markov chain, which is used to automatically generate sentences. \
This stores your messages in a combined form - they are never stored or outputted in full. When many messages are combined in this way it becomes \
difficult to reconstruct the original sentences, but it may still be possible to relate the data back to you. This data is never shared with any third parties.\n\n\
Please do not invite this bot to channels where sensitive or private topics are discussed. This bot carries no warranty, express or implied, and the owners/maintainers/\
providers of this bot take no responsibility for any consequences that may arise from its use in any way.'

groups = {}

# Standard commands
def start(bot, update):
    bot.send_message(update.message.chat_id, text=START_TEXT, parse_mode=telegram.ParseMode.MARKDOWN)

def privacy(bot, update):
    bot.send_message(update.message.chat_id, text=PRIVACY_TEXT, parse_mode=telegram.ParseMode.MARKDOWN)


# Case specific command
def generate(bot, update):
    chat_id = update.message.chat_id
    try:
        sentence = groups[chat_id].sentence()
        bot.send_message(chat_id, text=sentence)
    except KeyError:
        bot.send_message(chat_id, text="We don't have any chat information from this group yet!")

# General message handler
def message(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text

    # Ignore single word replies
    if ' ' in message:
        global groups
        if chat_id not in groups:
            groups[chat_id] = GroupInfo(chat_id)

        groups[chat_id].add_message(message)

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
                    groups[ast.literal_eval(chat_id)] = GroupInfo(chat_id, data[chat_id])
        except ValueError:
            logging.info("No JSON saved data found")

    # Register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler([Filters.text], message))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("privacy", privacy))
    dispatcher.add_handler(CommandHandler("generate", generate))

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

        else:
            logging.info("Unknown command")

if __name__ == '__main__':
    main()
