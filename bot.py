from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import json
import f
# Content of f.py
# # Module: f.py
# from telegram.ext.updater import Updater
# updater = Updater("Token", use_context=True)

ONESTO = 'onesto.txt'
PAP = 'pap.txt'
PPB = 'ppb.txt'
PUNTI = 'punteggio.txt'
CLASSIFICA = 'classifica.txt'

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Ciao, Benvenuto nel bot non ufficiale del fantacitorio. Scrivi help per vedere tutti i comandi.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
    /onesto     - squadra
    /pap        - squadra
    /ppb        - squadra
    /classifica - giocatori
    /punti      - tutti i politici""")

def onestoo(update: Update, context: CallbackContext):
    result = json.dumps(onesto)
    update.message.reply_text(result)

def papp(update: Update, context: CallbackContext):
    result = json.dumps(pap)
    update.message.reply_text(result)

def ppbb(update: Update, context: CallbackContext):
    result = json.dumps(ppb)
    update.message.reply_text(result)

def puntii(update: Update, context: CallbackContext):
    result = json.dumps(punti)
    update.message.reply_text(result)

def classificaa(update: Update, context: CallbackContext):
    result = json.dumps(classifica)
    update.message.reply_text(result)

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)

onesto = {}
file = open(ONESTO, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    fanfani = {
        'prezzo': int(campi[1])
    }
    onesto[nome] = fanfani
file.close()

pap = {}
file = open(PAP, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    fanfani = {
        'prezzo': int(campi[1])
    }
    pap[nome] = fanfani
file.close()

ppb = {}
file = open(PPB, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    fanfani = {
        'prezzo': int(campi[1])
    }
    ppb[nome] = fanfani
file.close()

punti = {}
file = open(PUNTI, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    p = {
        'punti': int(campi[1])
    }
    punti[nome] = p
file.close()

classifica = {}
file = open(CLASSIFICA, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    p = {
        'punti': int(campi[1])
    }
    classifica[nome] = p
file.close()

f.updater.dispatcher.add_handler(CommandHandler('start', start))
f.updater.dispatcher.add_handler(CommandHandler('onesto', onestoo))
f.updater.dispatcher.add_handler(CommandHandler('pap', papp))
f.updater.dispatcher.add_handler(CommandHandler('ppb', ppbb))
f.updater.dispatcher.add_handler(CommandHandler('punti', puntii))
f.updater.dispatcher.add_handler(CommandHandler('classifica', classificaa))
f.updater.dispatcher.add_handler(CommandHandler('help', help))
f.updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
f.updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
f.updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
f.updater.start_polling()
