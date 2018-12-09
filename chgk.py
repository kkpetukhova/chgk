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

with open('token.txt','r') as output:
    token = output.read()
    bot = telebot.TeleBot(str(token).strip())

current_shown_dates={}

iter_q = 0
curQ = {}
prevAnswer = ""
theme = ""
numPage = 0

@bot.message_handler(commands=['start', 'help'])
def bot_start(message):
    now = datetime.datetime.now() #Current date
    bot.send_message(message.chat.id, "Чтобы начать - напишите тему\nВопросы взяты из Базы вопросов «Что? Где? Когда?» \nhttps://db.chgk.info")

def PrintChoice(mode):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    if (mode == 'q'):
        answer_button = types.KeyboardButton(text="Answer")
        next_button = types.KeyboardButton(text="Next question")
        another_theme = types.KeyboardButton(text="Another theme")
    if (mode == 'a'):
        answer_button = types.KeyboardButton(text="Comment")
        next_button = types.KeyboardButton(text="Next question")
        another_theme = types.KeyboardButton(text="Another theme")
    keyboard.add(answer_button, next_button, another_theme)
    return keyboard

@bot.message_handler(regexp="Next question")
def PrintQuestion(message):
    global curQ
    keyboard = PrintChoice('q')
    curQ = QDictionary(message)
    if (curQ == 1):
        bot.send_message(message.chat.id, "Больше на эту тему нет вопросов. Напишите новую тему.")
    else:
        bot.send_message(message.chat.id, curQ.get("question"), reply_markup=keyboard)

@bot.message_handler(regexp="Comment")
def PrintAnswer(message):
    global curQ
    keyboard = PrintChoice('a')
    bot.send_message(message.chat.id, curQ.get("comment"), reply_markup=keyboard)


@bot.message_handler(regexp="Answer")
def PrintAnswer(message):
    global curQ
    keyboard = PrintChoice('a')
    bot.send_message(message.chat.id, curQ.get("answer"), reply_markup=keyboard)

@bot.message_handler(regexp="Another theme")
def AnotherTheme(message):
    bot.send_message(message.chat.id, "Напишите новую тему.")

def NewXML(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        with open('question.xml','wb') as output:
            for line in response: # files are iterable
                output.write(line)

@bot.message_handler(regexp="^(?!\/)[\w]+")
def ChooseTheme(message):
    global curQ, theme, numPage
    numPage = 0
    theme = message.text
    url = 'https://db.chgk.info/xml/search/questions/' + quote(theme) + '/types123/QC'
    #NewXML(url)
    keyboard = PrintChoice('q')
    curQ = QDictionary(message)
    if (curQ == 1):
        bot.send_message(message.chat.id, "Больше на эту тему нет вопросов. Напишите новую тему.")
    else:
        bot.send_message(message.chat.id, curQ.get("question"), reply_markup=keyboard)

def QDictionary(message):
    Qdict = {}
    global iter_q, prevAnswer
    i = 0
    tmp = 0
    tree = ET.parse('question.xml')
    numQuestions = xp.numQ(tree)
    if (iter_q == numQuestions):
        if (numQuestions >= 50):
            numPage = numPage + 1
            url = 'https://db.chgk.info/xml/search/questions/' + quote(theme) + '/types123/QC?page=' + numPage
            NewXML(url)
            tree = ET.parse('question.xml')
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

#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)


#@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
#def ignore(call):
#   bot.answer_callback_query(call.id, text="")


bot.polling()
