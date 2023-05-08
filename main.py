"""
    A Bot to automatically add nearby friends in the background on facebook

    #random hash: 0413be8e0d87f6a488fe5ac3c1b3ff4b
"""
import configparser
from playwright.sync_api import sync_playwright
import time
#CONFIG PARSER INIT
config = configparser.RawConfigParser()
config.read("config.ini")

USERNAME = config.get("Facebook Account","USERNAME")
PASSWORD = config.get("Facebook Account","PASSWORD")

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

      #ADD SUGGESTED
      page.goto("https://www.facebook.com/friends/suggestions")
      page.wait_for_load_state()
      # elements = page.get_by_text("Ajouter")
      elements = page.query_selector_all("span:contains('Ajouter')")
      for element in elements:
            print(element.text_content())

      #ADD SEARCH QUERY

      #Search in facebook a random string

      #Go to Personnes

      #Apply a Search term in Ville "Paris"

      