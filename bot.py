from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
from collections import OrderedDict
import requests

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

t1 = "/onesto"
t2 = "/pap"
t3 = "/ppb"
t5 = "/punti"
t4 = "/classifica"

PROVA = 21

punti_onesto = 0
punti_pap = 0
punti_ppb = 0

def dict_or_OrdDict_to_formatted_str(OD, mode='dict', s="", indent=' '*4, level=0):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    def fstr(s):
        return s if is_number(s) else '"%s"'%s
    if mode != 'dict':
        kv_tpl = '("%s", %s)'
        ST = 'OrderedDict([\n'; END = '])'
    else:
        kv_tpl = '"%s": %s'
        ST = '{\n'; END = '}'
    for i,k in enumerate(OD.keys()):
        if type(OD[k]) in [dict, OrderedDict]:
            level += 1
            s += (level-1)*indent+kv_tpl%(k,ST+dict_or_OrdDict_to_formatted_str(OD[k], mode=mode, indent=indent, level=level)+(level-1)*indent+END)
            level -= 1
        else:
            s += level*indent+kv_tpl%(k,fstr(OD[k]))
        if i!=len(OD)-1:
            s += ","
        s += "\n"
    return s


def start(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(t1)], [KeyboardButton(t2)], [KeyboardButton(t3)], [KeyboardButton(t4)], [KeyboardButton(t5)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, Benvenuto nel bot non ufficiale del fantacitorio. Scrivi /help per vedere tutti i comandi.", reply_markup=ReplyKeyboardMarkup(buttons))

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
    /onesto     - squadra
    /pap        - squadra
    /ppb        - squadra
    /classifica - giocatori
    /punti      - tutti i politici""")

def onestoo(update: Update, context: CallbackContext):
    onesto_1 = " "+(str(onesto).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("prezzo", "").replace(":", " "))
    update.message.reply_text(onesto_1)

def papp(update: Update, context: CallbackContext):
    pap_1 = " "+(str(pap).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("prezzo", "").replace(":", " "))
    update.message.reply_text(pap_1)

def ppbb(update: Update, context: CallbackContext):
    ppb_1 = " "+(str(ppb).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("prezzo", "").replace(":", " "))
    update.message.reply_text(ppb_1)

def puntii(update: Update, context: CallbackContext):
    # o_pol_1 = dict_or_OrdDict_to_formatted_str(o_pol)
    # o_pol_2 = (str(o_pol_1).replace("\"", "").replace(",", "").replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("punti", "").replace(":", " "))
    # update.message.reply_text(o_pol_2)
    punti_1 = " "+(str(punti).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("punti", "").replace(":", " "))
    update.message.reply_text(punti_1)

def classificaa(update: Update, context: CallbackContext):
    res_1 = dict_or_OrdDict_to_formatted_str(res)
    res_2 = (str(res_1).replace("\"", "").replace(",", ""))
    update.message.reply_text(res_2)

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
    if nome in punti:
        punti[nome]['punti'] = int(punti[nome]['punti']) + int(campi[1])
    else:
        p = {
            'punti': int(campi[1])
        }
        punti[nome] = p
file.close()

classifica = {}

for politico in punti:
    for membro in onesto:
        if membro == politico:
            punti_p = punti[politico]['punti']
            punti_onesto = punti_onesto + punti_p
            classifica.update({"ONESTO": punti_onesto})

for politico in punti:
    for membro in pap:
        if membro == politico:
            punti_r = punti[politico]['punti']
            punti_pap = punti_pap + punti_r
            classifica.update({"PAP": punti_pap})

for politico in punti:
    for membro in ppb:
        if membro == politico:
            punti_q = punti[politico]['punti']
            punti_ppb = punti_ppb + punti_q
            classifica.update({"PPB": punti_ppb})

res = OrderedDict(reversed(list(classifica.items())))
# o_pol = OrderedDict(reversed(list(punti.items())))

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
