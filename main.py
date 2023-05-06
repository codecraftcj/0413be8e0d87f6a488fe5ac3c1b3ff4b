"""
    A Bot to automatically add nearby friends in the background on facebook
"""
import configparser
from playwright.sync_api import sync_playwright
import time
#CONFIG PARSER INIT
config = configparser.RawConfigParser()
config.read("config.ini")

USERNAME = config.get("Facebook Account","USERNAME")
PASSWORD = config.get("Facebook Account","PASSWORD")
USERNAME = "TEST"
PASSWORD = "TEST"
with sync_playwright() as playwright:

      #BOT LOGIN
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=False) #switch to False when debugging
        page = browser.new_page()
        page.goto("https://www.facebook.com/")
        time.sleep(5)
        page.query_selector("input[id='email']").click()
        page.keyboard.type(USERNAME)
        page.query_selector("input[id='pass']").click()
        page.keyboard.type(PASSWORD)
        page.query_selector("button[type='submit']").click()
        time.sleep(10)