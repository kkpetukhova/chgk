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

bot = telebot.TeleBot("")
current_shown_dates={}

iter_q = 0

@bot.message_handler(commands=['start', 'help'])
def bot_start(message):
    now = datetime.datetime.now() #Current date
    bot.send_message(message.chat.id, "Чтобы начать - напиши тему\n/next : следующий вопрос\n/answer : ответ на текущий вопрос\nВопросы взяты из Базы вопросов «Что? Где? Когда?» \nhttps://db.chgk.info")


@bot.message_handler(regexp="^(?!\/)[\w]+")
def ChooseTheme(message):
    theme = message.text
    global iter_q
    url = 'https://db.chgk.info/xml/search/questions/' + quote(theme) + '/types123/QC'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        with open('question.xml','wb') as output:
            for line in response: # files are iterable
                output.write(line)
    tree = ET.parse('question.xml')
    for node in tree.iter('question'):
        for elem in node.iter():
            if not elem.tag==node.tag:
                if (elem.tag == 'Question'):
                    bot.send_message(message.chat.id, "{}: {}".format(elem.tag, elem.text))
                    iter_q = 1
            if (iter_q == 1):
                break
        if (iter_q == 1):
            break

@bot.message_handler(commands=['next'])
def NextQuestion(message):
    global iter_q
    tmp = 0
    tree = ET.parse('question.xml')
    i = 0
    for node in tree.iter('question'):
        for elem in node.iter():
            if (not elem.tag==node.tag) and (elem.tag == 'Question'):
                if i == iter_q:
                    bot.send_message(message.chat.id, "{}: {}".format(elem.tag, elem.text))
                    iter_q = iter_q + 1
                    tmp = 1
                i = i + 1
            if (tmp == 1): break

@bot.message_handler(commands=['answer'])
def NextQuestion(message):
    global iter_q
    tree = ET.parse('question.xml')
    i = 0
    tmp = 0
    for node in tree.iter('question'):
        for elem in node.iter():
            if (not elem.tag==node.tag) and (elem.tag == 'Answer'):
                if i == iter_q - 1:
                    bot.send_message(message.chat.id, "{}: {}".format(elem.tag, elem.text))
                    tmp = 1
                i = i + 1
        if (tmp == 1): break

@bot.message_handler(commands=['date'])
def check_date(message):
    saved_day = message.date
    bot.send_message(message.chat.id, datetime.datetime.fromtimestamp(saved_day).strftime('%Y-%m-%d %H:%M:%S'))

#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#    bot.reply_to(message, message.text)


@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")


bot.polling()
