#!/usr/local/bin/python3
# coding=utf-8
import telebot
from telebot import types
import datetime

import urllib
from urllib.request import urlopen
import re

import urllib.request
from urllib.request import urlopen
import urllib.parse
import requests
from urllib.parse import quote
import xml.etree.ElementTree as ET

import xmlParse as xp
import keyboard as kb

with open('token.txt','r') as output:
    token = output.read()
    bot = telebot.TeleBot(str(token).strip())

current_shown_dates={}

iter_q = 0
irand = 0
curQ = {}
prevAnswer = ""
theme = ""
numPage = 0
rand = 0
gap = "____________________________________________________________"
xmlname = ""


@bot.message_handler(commands=['start', 'help'])
def bot_start(message):
    global xmlname
    now = datetime.datetime.now() #Current date
    keyboard = kb.PrintChoice('s');
    bot.send_message(message.chat.id, "Вопросы взяты из Базы вопросов «Что? Где? Когда?» \nhttps://db.chgk.info", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "answer":
            PrintAnswer(call.message)
        if call.data == "new_theme":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Напишите новую тему.")
        if call.data == "next_question":
            PrintQuestion(call.message)
        if call.data == "comment":
            PrintComment(call.message)
        if call.data == "rand_question":
            RandomQuestion(call.message)

def RandomQuestion(message):
    global curQ, rand, irand
    rand = 1
    url = 'https://db.chgk.info/xml/random'
    xmlname = xp.GetXMLName(message)
    irand = irand + 1
    if irand == 20 or irand == 1:
        xp.NewXML(url, xmlname)
        irand = 1
    keyboard = kb.PrintChoice('r')
    curQ = QDictionary(message)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text = curQ.get("question"))
    bot.send_message(message.chat.id, gap, reply_markup=keyboard)


def PrintQuestion(message):
    global curQ
    keyboard = kb.PrintChoice('q')
    curQ = QDictionary(message)
    if (curQ == 1):
        bot.send_message(message.chat.id, text = "Больше на эту тему нет вопросов. Напишите новую тему.")
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text = curQ.get("question"))
        bot.send_message(message.chat.id, gap, reply_markup=keyboard)


def PrintComment(message):
    global curQ, rand
    if rand == 1:
        keyboard = kb.PrintChoice('rc')
    else:
        keyboard = kb.PrintChoice('c')
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text = curQ.get("comment"))
    bot.send_message(message.chat.id, gap, reply_markup=keyboard)


def PrintAnswer(message):
    global curQ
    if rand == 1:
        keyboard = kb.PrintChoice('ra')
    else:
        keyboard = kb.PrintChoice('a')
    #bot.send_message(message.chat.id, curQ.get("answer"), reply_markup=keyboard)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text = curQ.get("answer"))
    bot.send_message(message.chat.id, gap, reply_markup=keyboard)


@bot.message_handler(regexp="^(?!\/)[\w]+")
def ChooseTheme(message):
    global curQ, theme, numPage, rand
    rand = 0
    numPage = 0
    theme = message.text
    url = 'https://db.chgk.info/xml/search/questions/' + quote(theme) + '/types123/QC'
    xmlname = xp.GetXMLName(message)
    xp.NewXML(url, xmlname)
    keyboard = kb.PrintChoice('q')
    curQ = QDictionary(message)
    if (curQ == 1):
        bot.send_message(message.chat.id, "Больше на эту тему нет вопросов. Напишите новую тему.")
    else:
        bot.send_message(message.chat.id, curQ.get("question"))
        bot.send_message(message.chat.id, gap, reply_markup=keyboard)


def QDictionary(message):
    Qdict = {}
    global iter_q, prevAnswer
    i = 0
    tmp = 0
    xmlname = xp.GetXMLName(message)
    tree = ET.parse(xmlname)
    numQuestions = xp.numQ(tree)
    if (iter_q == numQuestions):
        if (numQuestions >= 50):
            numPage = numPage + 1
            url = 'https://db.chgk.info/xml/search/questions/' + quote(theme) + '/types123/QC?page=' + numPage
            xmlname = xp.GetXMLName(message)
            xp.NewXML(url, xmlname)
            tree = ET.parse(xmlname)
        else:
            #we don't have q for current theme
            iter_q = 0
            return 1
    for node in tree.iter('question'):
        if i == iter_q:
            tmp = 1
            iter_q = iter_q + 1
            for elem in node.iter():
                if (not elem.tag==node.tag): #and (elem.tag == 'Question'):  "{}: {}".format(elem.tag, elem.text)
                    if (elem.tag == 'Question'):
                            Qdict['question'] = "{}: {}".format(elem.tag, elem.text)
                    if (elem.tag == 'Answer'):
                        Qdict['answer'] = "{}: {}".format(elem.tag, elem.text)
                        if (prevAnswer == Qdict.get("answer")): tmp = 0
                    if (elem.tag == 'Comments'):
                            Qdict['comment'] = "{}: {}".format(elem.tag, elem.text)
        i = i + 1
        if (tmp == 1): break
    prevAnswer = Qdict.get("answer")
    return Qdict

@bot.message_handler(commands=['date'])
def check_date(message):
    saved_day = message.date
    bot.send_message(message.chat.id, datetime.datetime.fromtimestamp(saved_day).strftime('%Y-%m-%d %H:%M:%S'))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


#@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
#def ignore(call):
#   bot.answer_callback_query(call.id, text="")


bot.polling()
