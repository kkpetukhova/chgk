#!/usr/local/bin/python3
# coding=utf-8
import urllib
from urllib.request import urlopen
import re

import urllib.request
from urllib.request import urlopen
import urllib.parse
import requests
from urllib.parse import quote
import xml.etree.ElementTree as ET


def numQ(tree):
    i = 0
    for node in tree.iter('question'):
        i = i + 1
    return i


def NewXML(url, xmlname):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        with open(xmlname,'wb') as output:
            for line in response: # files are iterable
                output.write(line)

def GetXMLName(message):
    xmlname = "question_" + str(message.chat.id) + ".xml"
    return xmlname
