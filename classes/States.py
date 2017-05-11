# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 14:17:07 2017

@author: Donzok
"""
from enum import Enum

class BotStates(Enum):
    AWAITING_LOCATION = 1
    AWAITING_ZOOM = 2
