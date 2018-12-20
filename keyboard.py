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


def PrintChoice(mode):
    keyboard = types.InlineKeyboardMarkup()
    if (mode == 'q'):
        answer_button = types.InlineKeyboardButton(text="Ответ", callback_data="answer")
        next_button = types.InlineKeyboardButton(text="Следующий вопрос", callback_data="next_question")
        new_theme = types.InlineKeyboardButton(text="Задать новую тему", callback_data="new_theme")
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        keyboard.add(answer_button, next_button)
        keyboard.add(new_theme, random_button)
    if (mode == 'a'):
        comment_button = types.InlineKeyboardButton(text="Комментарий", callback_data="comment")
        next_button = types.InlineKeyboardButton(text="Следующий вопрос", callback_data="next_question")
        new_theme = types.InlineKeyboardButton(text="Задать новую тему", callback_data="new_theme")
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        keyboard.add(comment_button, next_button)
        keyboard.add(random_button, new_theme)
    if (mode == 'c'):
        next_button = types.InlineKeyboardButton(text="Следующий вопрос", callback_data="next_question")
        new_theme = types.InlineKeyboardButton(text="Задать новую тему", callback_data="new_theme")
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        keyboard.add(next_button)
        keyboard.add(random_button, new_theme)
    if (mode == 's'):
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        new_theme = types.InlineKeyboardButton(text="Задать новую тему", callback_data="new_theme")
        keyboard.add(random_button, new_theme)
    if (mode == 'r'):
        answer_button = types.InlineKeyboardButton(text="Ответ", callback_data="answer")
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        new_theme = types.InlineKeyboardButton(text="Задать тему", callback_data="new_theme")
        keyboard.add(answer_button)
        keyboard.add(random_button, new_theme)
    if (mode == 'ra'):
        comment_button = types.InlineKeyboardButton(text="Комментарий", callback_data="comment")
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        new_theme = types.InlineKeyboardButton(text="Задать тему", callback_data="new_theme")
        keyboard.add(comment_button)
        keyboard.add(random_button, new_theme)
    if (mode == 'rc'):
        random_button = types.InlineKeyboardButton(text="Случайный вопрос", callback_data="rand_question")
        new_theme = types.InlineKeyboardButton(text="Задать тему", callback_data="new_theme")
        keyboard.add(random_button, new_theme)
    return keyboard
