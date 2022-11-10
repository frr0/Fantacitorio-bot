from telegram.ext.updater import Updater
import os
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

TEAM1 = 'Gianluca.txt'
TEAM2 = 'Francesco.txt'
TEAM3 = 'Fra.txt'
PUNTI = 'data.txt'
CLASSIFICA = 'classifica.txt'

t1 = "/team1"
t2 = "/team2"
t3 = "/team3"
t5 = "/punti"
t4 = "/classifica"

PROVA = 21

punti_team1 = 0
punti_team2 = 0
punti_team3 = 0

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


def _start(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(t1)], [KeyboardButton(t2)], [KeyboardButton(t3)], [KeyboardButton(t4)], [KeyboardButton(t5)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, Benvenuto nel bot non ufficiale del fantacitorio. Scrivi /help per vedere tutti i comandi.", reply_markup=ReplyKeyboardMarkup(buttons))

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
    /team1      - squadra
    /team2      - squadra
    /team3      - squadra
    /classifica - giocatori
    /punti      - tutti i politici""")

def _team1(update: Update, context: CallbackContext):
    team1_1 = " "+(str(team1).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("prezzo", "").replace(":", " "))
    # bot.sendPhoto(chat_id, photo=open('/home/fra/projects/Fantacitorio-bot/team1.jpg', 'rb'))
    update.message.reply_text(team1_1)

def _team2(update: Update, context: CallbackContext):
    team2_1 = " "+(str(team2).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("prezzo", "").replace(":", " "))
    # bot.sendPhoto(chat_id, photo=open('/home/fra/projects/Fantacitorio-bot/team2.jpg', 'rb'))
    update.message.reply_text(team2_1)

def _team3(update: Update, context: CallbackContext):
    team3_1 = " "+(str(team3).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("prezzo", "").replace(":", " "))
    # bot.sendPhoto(chat_id, photo=open('/home/fra/projects/Fantacitorio-bot/team3.jpg', 'rb'))
    update.message.reply_text(team3_1)

def _punti(update: Update, context: CallbackContext):
    # o_pol_1 = dict_or_OrdDict_to_formatted_str(o_pol)
    # o_pol_2 = (str(o_pol_1).replace("\"", "").replace(",", "").replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("punti", "").replace(":", " "))
    # update.message.reply_text(o_pol_2)
    punti_1 = " "+(str(punti).replace("{","").replace("}", "").replace("'", "").replace(",", "\n").replace("punti", "").replace(":", " "))
    update.message.reply_text(punti_1)

def _classifica(update: Update, context: CallbackContext):
    os.system("snscrape --jsonl --progress --max-results 200 twitter-search \"from:Fanta_citorio\" > tweets.json && cat tweets.json | jq '.content' > data.txt")
    res_1 = dict_or_OrdDict_to_formatted_str(res)
    res_2 = (str(res_1).replace("\"", "").replace(",", ""))
    update.message.reply_text(res_2)

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)

team1 = {}
file = open(TEAM1, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    fanfani = {
        'prezzo': int(campi[1])
    }
    team1[nome] = fanfani
file.close()

team2 = {}
file = open(TEAM2, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    fanfani = {
        'prezzo': int(campi[1])
    }
    team2[nome] = fanfani
file.close()

team3 = {}
file = open(TEAM3, 'r')
for line in file:
    campi = line.rstrip().split(',')
    nome = campi[0]
    fanfani = {
        'prezzo': int(campi[1])
    }
    team3[nome] = fanfani
file.close()

punti = {}
file = open(PUNTI, 'r')
for line in file:
    campi_dati = line.rstrip().split(' ')
    if campi_dati[1] == 'PUNTI':
        nome = campi_dati[4]
        if nome == 'SQUADRE:':
            break
        campi = nome.split('\\')
        nome = campi[0]
        campi_dati = campi_dati[0].split('"')
        if nome in punti:
            punti[nome]['punti'] = int(punti[nome]['punti']) + int(campi_dati[1])
        else:
            p = {
                'punti': int(campi_dati[1])
            }
            punti[nome] = p
    elif campi_dati[2] == 'PUNTI':
        nome = campi_dati[5]
        campi = nome.split('\\')
        nome = campi[0]
        campi_dati = campi_dati[1].split('"')
        if nome in punti:
            punti[nome]['punti'] = int(punti[nome]['punti']) + int(campi_dati[2])
        else:
            p = {
                'punti': int(campi_dati[0])
            }
            punti[nome] = p
    
file.close()

classifica = {}

for politico in punti:
    for membro in team1:
        if membro == politico:
            punti_1 = punti[politico]['punti']
            punti_team1 = punti_team1 + punti_1
            classifica.update({"team1 (Gianluca)": punti_team1})

for politico in punti:
    for membro in team2:
        if membro == politico:
            punti_2 = punti[politico]['punti']
            punti_team2 = punti_team2 + punti_2
            classifica.update({"team2 (Francesco)": punti_team2})

for politico in punti:
    for membro in team3:
        if membro == politico:
            punti_3 = punti[politico]['punti']
            punti_team3 = punti_team3 + punti_3
            classifica.update({"team3 (Fra Re.)": punti_team3})

# res = OrderedDict(reversed(list(classifica.items())))
res = OrderedDict((list(classifica.items())))
# o_pol = OrderedDict(reversed(list(punti.items())))

f.updater.dispatcher.add_handler(CommandHandler('start', _start))
f.updater.dispatcher.add_handler(CommandHandler('team1', _team1))
f.updater.dispatcher.add_handler(CommandHandler('team2', _team2))
f.updater.dispatcher.add_handler(CommandHandler('team3', _team3))
f.updater.dispatcher.add_handler(CommandHandler('punti', _punti))
f.updater.dispatcher.add_handler(CommandHandler('classifica', _classifica))
f.updater.dispatcher.add_handler(CommandHandler('help', help))
f.updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
f.updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
f.updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
f.updater.start_polling()
