# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 23:15:01 2017

@author: Donzok
"""
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import uuid


def _fill_email(driver, iitc_mail):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of(driver.find_element_by_xpath("//input[@type='email']")))

        email_input = driver.find_element_by_xpath("//input[@type='email']")
        email_input.clear()
        email_input.send_keys(iitc_mail)

        button = driver.find_element_by_id("identifierNext")
        button.click()
    except:
        print("Auto-sign in or email filled")


def _fill_password(driver, iitc_pass):
    try:
        WebDriverWait(driver, 5).until(
             EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))

        passwd_input = driver.find_element_by_xpath("//input[@type='password']")
        passwd_input.clear()
        passwd_input.send_keys(iitc_pass)
        passwd_input.send_keys(Keys.ENTER)
    except Exception as e:
        raise e


def login_if_necessary(driver, iitc_mail, iitc_pass):
    if "Welcome to Ingress." in driver.page_source:

        sign_in_button = driver.find_element_by_xpath("//div[contains(@class, 'unselectable')][1]/a")
        sign_in_button.click()

        _fill_email(driver, iitc_mail)
        _fill_password(driver, iitc_pass)
    else:
        print("No need")

    try:
        WebDriverWait(driver, 10).until(lambda driver:
                                        (driver.current_url.startswith("https://www.ingress.com/intel" or
                                         driver.current_url.startswith("https://ingress.com/intel"))))
    except:
        print("Couldn't reach intel page")
        print(driver.current_url)

    #WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, 'loading_msg_text')))