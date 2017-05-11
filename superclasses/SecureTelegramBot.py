# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:42:55 2017

@author: Donzok
"""
import json

import requests
import telepot


class SecureTelegramBot(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(SecureTelegramBot, self).__init__(*args, **kwargs)

        self._v_api_key = None
        self._rocks_api_key = None

        pass
    
    async def on_chat_message(self, msg):
        pass

    async def on__idle(self, event):
        self.close()
            
    async def user_has_rights(self, user_id):
        v_url = "https://v.enl.one/api/v1/search?telegramId={0}&apikey={1}".format(user_id, self._v_api_key)
        rocks_url = "https://enlightened.rocks/api/user/status/{0}?apikey={1}".format(user_id, self._rocks_api_key)
        
        response = requests.get(v_url)
        v_content = json.loads(response.content.decode("utf8"))
        
        response = requests.get(rocks_url)
        rocks_content = json.loads(response.content.decode("utf-8"))
        
        res = False        
        
        if v_content['status'] == "ok" and len(v_content['data']):    
            await self.sender.sendMessage('Hi, you are in V. Your V agent name is {0}, '
                                          'your level is {1} and you have {2} points.'
                                          .format(v_content['data'][0]['agent'],
                                                  v_content['data'][0]['vlevel'],
                                                  v_content['data'][0]['vpoints']))
            
            res = (v_content['status'] == "ok" 
                    and v_content['data'][0]['verified'] 
                    and not v_content['data'][0]['blacklisted']
                    and not v_content['data'][0]['flagged']
                    and not v_content['data'][0]['quarantine'])
                    
        if len(rocks_content):
            await self.sender.sendMessage('Hi, you are in Rocks. Your Rocks agent name is {0}, '
                                          'and your "verify" status is:{1}.'
                                          .format(rocks_content['agentid'],
                                                  rocks_content['verified']))
            
            res = rocks_content['verified']
        
        return res