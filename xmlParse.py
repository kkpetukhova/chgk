#!/usr/local/bin/python3
# coding=utf-8
import xml.etree.ElementTree as ET


def numQ(tree):
    i = 0
    for node in tree.iter('question'):
        i = i + 1
    return i
