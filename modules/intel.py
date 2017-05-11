# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:15:01 2017

@author: Donzok
"""
import configparser
import uuid

from .iitc import *
from .login import login_if_necessary

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


_intel_url_base = "https://www.ingress.com/intel"


def _get_intel_url(coordinates, zoom=16):
    return _intel_url_base + "?ll={0},{1}&z={2}".format(coordinates[0], coordinates[1], zoom)


def prepare_intel(coordinates, iitc_mail, iitc_pass, zoom=16):
    config = configparser.ConfigParser()
    config.read("config.ini")
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    )
    driver = webdriver.PhantomJS(executable_path=config["DEFAULT"]["phantomjs_path"], desired_capabilities=dcap)
    # driver = webdriver.Chrome(executable_path=r"D:\Downloads\chromedriver.exe")

    try:
        driver.set_window_size(config["SCREEN"]["width"], config["SCREEN"]["height"])

        print(_get_intel_url(coordinates, zoom))
        driver.get(_get_intel_url(coordinates, zoom))

        login_if_necessary(driver, iitc_mail, iitc_pass)

        prepare_iitc(driver, config)

        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, "svq_loaded")))

        driver.execute_script("document.getElementById('scrollwrapper').style.display = 'none'")
        driver.execute_script("document.getElementsByClassName('leaflet-control-container')[0].style.display = 'none'")
        driver.execute_script("document.getElementById('privacycontrols').style.display = 'none'")
        driver.execute_script("document.getElementById('sidebartoggle').style.display = 'none'")
        driver.execute_script("document.getElementById('updatestatus').style.display = 'none'")

        return True, driver
    except Exception as e:
        print(e)

        return False, driver


def screenshot(driver):
    filename = "screenshots/{0}.png".format(str(uuid.uuid1()))

    driver.get_screenshot_as_file(filename)

    driver.close()

    return filename