#!/usr/bin/env python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import CineHandler
import os

# Telegram Token #
telegram_token = [line.split() for line in open('keys')][0][0]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

"""
help - Help!
espaciomediterraneo - Cartelera del cine del Espacio Mediterraneo
mandarache - Cartelera del cine del Mandarache
eltiro - Cartelera del cine de El Tiro
condomina - Cartelera del cine de la Nueva Condomina
thader - Cartelera del cine del Thader
"""
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

# /start #
def start(bot, update):
    update.message.reply_text('¡Hola!\n- - - - - - - -\n')
    help(bot, update)

# /help #
def help(bot, update):
    help_text = "Con este Bot podrás consultar la cartelera de los cines listados a continuación:\n\n/espaciomediterraneo - Cartelera del cine del Espacio Mediterraneo\n/mandarache - Cartelera del cine del Mandarache\n/eltiro - Cartelera del cine de El Tiro\n/condomina - Cartelera del cine de la Nueva Condomina\n/thader - Cartelera del cine del Thader\n\nSi deseas agregar un cine a la lista de contactos mandame un email:\n \
        alex.ortiz.garcia@gmail.com\n\nEspero que te guste AchoBot! "
    update.message.reply_text(help_text)

# /espaciomediterraneo #
def espaciomediterraneo(bot, update):
    cine = "Espacio Mediterraneo:"
    url = "http://www.neocine.es/cine/4/espacio-mediterraneo--cartagena-/lang/es"
    update.message.reply_text(CineHandler.getMoviesFromNeocineWebsite(cine,url))

# /mandarache #
def mandarache(bot, update):
    cine = "Mandarache:"
    url = "http://www.neocine.es/cine/6/mandarache--cartagena-/lang/es"
    update.message.reply_text(CineHandler.getMoviesFromNeocineWebsite(cine, url))

# /eltiro #
def eltiro(bot, update):
    cine = "El Tiro:"
    url = "http://www.neocine.es/cine/5/hd-digital-el-tiro--murcia-/lang/es"
    update.message.reply_text(CineHandler.getMoviesFromNeocineWebsite(cine, url))

# /condomina #
def condomina(bot, update):
    cine = "Nueva Condomina:"
    url = "http://www.cinerama.es/cartelera/cine/nueva-condomina/"
    update.message.reply_text(CineHandler.getMoviesFromCineramaWebsite(cine, url))

# /thader #
def thader(bot, update):
    cine = "Thader:"
    url = "http://www.neocine.es/cine/9/thader--murcia-/lang/es"
    update.message.reply_text(CineHandler.getMoviesFromNeocineWebsite(cine, url))

# random text received #
def no_command(bot, update):
    update.message.reply_text("¡Utiliza /help para ver la lista de comandos!")

# error handle -> log #
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


# main loop #
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_token)
    PORT = int(os.environ.get('PORT', '5000'))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=telegram_token)
    updater.bot.setWebhook("https://achocine.herokuapp.com/" + telegram_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("espaciomediterraneo", espaciomediterraneo))
    dp.add_handler(CommandHandler("mandarache", mandarache))
    dp.add_handler(CommandHandler("eltiro", eltiro))
    dp.add_handler(CommandHandler("condomina", condomina))
    dp.add_handler(CommandHandler("thader", thader))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, no_command))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()