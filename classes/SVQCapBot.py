# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:42:55 2017

@author: Donzok
"""

import configparser
import json
import logging
import os

import telepot

import modules.intel as intel
from superclasses.SecureTelegramBot import SecureTelegramBot
from .States import BotStates
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import classes.Utils as Utils


class SVQCapBot(SecureTelegramBot):
    def __init__(self, *args, **kwargs):
        super(SVQCapBot, self).__init__(*args, **kwargs)

        self._v_api_key = None
        self._rocks_api_key = None
        self.iitc_mail = None
        self.iitc_pass = None
        self.bot_state = BotStates.AWAITING_LOCATION
        self.location = None

        with open('files/security.json', 'r') as security_file:
            security_json = json.load(security_file)
            self._v_api_key = security_json['v_api_key']
            self._rocks_api_key = security_json['rocks_api_key']

        config = configparser.ConfigParser()
        config.read("config.ini")

        self.iitc_mail = config['IITC']['mail']
        self.iitc_pass = config['IITC']['pass']

        self.logger = logging.getLogger('svqcap-bot')
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('./svqcap_bot.log')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        print(chat_id)

        print(self.bot_state)

        if content_type == "location":
            keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="16",
                                          request_contact=False,
                                          request_location=False),
                           KeyboardButton(text="15",
                                          request_contact=False,
                                          request_location=False),
                           KeyboardButton(text="14",
                                          request_contact=False,
                                          request_location=False)
                           ],
                          [KeyboardButton(text="12",
                                          request_contact=False,
                                          request_location=False),
                           KeyboardButton(text="10",
                                          request_contact=False,
                                          request_location=False),
                           KeyboardButton(text="8",
                                          request_contact=False,
                                          request_location=False)],
                          [KeyboardButton(text="Cancel",
                                          request_contact=False,
                                          request_location=False)]],
                resize_keyboard=True,
                one_time_keyboard=True,
                selective=True
            )

            self.location = (msg['location']['latitude'], msg['location']['longitude'])

            self.bot_state = BotStates.AWAITING_ZOOM
            await self.sender.sendMessage("Select the zoom level (or write your desired zoom between 3 and 17)", reply_markup=keyboard)

        elif content_type == "text" and self.bot_state == BotStates.AWAITING_ZOOM and self.location:
            remove_keyboard = ReplyKeyboardRemove(remove_keyboard=True, selective=False)

            try:
                user_input = msg['text'].rstrip('\r\n')
            except ValueError:
                await self.sender.sendMessage('It seems that your message is invalid. I\'m sorry', reply_markup=remove_keyboard)
                return

            if user_input == "Cancel":
                self.bot_state = BotStates.AWAITING_LOCATION
                await self.sender.sendMessage("Ok, I'll wait for you to send me another location. See you soon!",
                                              reply_markup=remove_keyboard)
            elif Utils.is_valid_int(user_input):
                await  self.sender.sendMessage("Hang on, I'll take your screenshot and send to you in a few seconds.", reply_markup=remove_keyboard)

                (res, driver) = intel.prepare_intel((self.location[0], self.location[1]),
                                                    self.iitc_mail, self.iitc_pass, int(user_input))

                if res:
                    screenshot = intel.screenshot(driver)

                    with open(screenshot, 'rb') as Screenshot:
                        await self.sender.sendPhoto(Screenshot)

                    os.remove(screenshot)
                    self.close()
                else:
                    screenshot = intel.screenshot(driver)

                    await self.sender.sendMessage("I'm so sorry but there was an error taking your screenshot, "
                                                  "please try again later or contact my creator @d0nzok.", parse_mode='Markdown')
                    self.close()
            else:
                self.bot_state = BotStates.AWAITING_ZOOM

                keyboard = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="16",
                                              request_contact=False,
                                              request_location=False),
                               KeyboardButton(text="15",
                                              request_contact=False,
                                              request_location=False),
                               KeyboardButton(text="14",
                                              request_contact=False,
                                              request_location=False)
                               ],
                              [KeyboardButton(text="12",
                                              request_contact=False,
                                              request_location=False),
                               KeyboardButton(text="10",
                                              request_contact=False,
                                              request_location=False),
                               KeyboardButton(text="8",
                                              request_contact=False,
                                              request_location=False)],
                              [KeyboardButton(text="Cancel",
                                              request_contact=False,
                                              request_location=False)]],
                    resize_keyboard=True,
                    one_time_keyboard=True,
                    selective=True
                )

                await self.sender.sendMessage("I'm sorry, but I need you to select one of the zoom levels in the "
                                              "keyboard below or write a zoom level between 3 and 17",
                                              reply_markup=keyboard)

        elif content_type == "text" and self.bot_state == BotStates.AWAITING_LOCATION:
            remove_keyboard = ReplyKeyboardRemove(remove_keyboard=True, selective=False)
            await self.sender.sendMessage("I'm sorry, but I need you to send me a location first, you can do it by "
                                          "clicking the 'attatch' button and selecting 'location'",
                                          reply_markup=remove_keyboard)

    async def on__idle(self, event):
        self.close()