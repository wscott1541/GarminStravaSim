#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 16:44:51 2022

@author: willscott
"""

#from html.parser import HTMLParser

import os
import codecs


def load_notes_html(activity_id):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, 'Notes/note_{}.html'.format(activity_id))
    
    if os.path.exists(filename):
    
    #page = urllib.urlopen(filename).read()
        page = codecs.open(filename, 'r', 'utf-8').read()
    else:
        page = ''
        
    
    return page
    

