# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:15:01 2017

@author: Donzok
"""
import requests
import json
import os


def prepare_iitc(driver, config):
    dir = os.path.dirname(__file__)
    iitc_plugin = 'https://static.iitc.me/build/release/total-conversion-build.user.js'
    loaded_plugin = os.path.join(dir, '../js/iitc_plugin_map_loaded.js')

    local_storages = json.loads(config["IITC"]["plugins_config"])

    for local_storage in local_storages:
        inject_local_storage(driver, local_storage)

    inject_plugin(driver, iitc_plugin)
    inject_plugin_file(driver, loaded_plugin)

    iitc_plugins = json.loads(config["IITC"]["iitc_plugins"])

    for plugin in iitc_plugins:
        inject_plugin(driver, plugin)


def inject_local_storage(driver, local_storage):
    driver.execute_script("localStorage.setItem('{0}', '{1}')"
                          .format(local_storage["key"], local_storage["value"]))


def inject_plugin(driver, iitc_plugin):
    file = requests.get(iitc_plugin)

    driver.execute_script(file.text)

def inject_plugin_file(driver, path):
    file = open(path, 'r')

    driver.execute_script(file.read())