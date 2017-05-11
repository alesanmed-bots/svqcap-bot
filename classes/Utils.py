# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:42:55 2017

@author: Donzok
"""

def is_valid_int(string):
    try:
        number = int(string)
        return 3 < number < 18
    except ValueError:
        return False
