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
      # page.goto("https://www.facebook.com/friends/suggestions")
      # page.wait_for_load_state()
      # # elements = page.get_by_text("Ajouter")
      # elements = page.query_selector_all("span:contains('Ajouter')")
      # for element in elements:
      #       print(element.text_content())

      #ADD SEARCH QUERY
      
      #Search in facebook a random string
      """
      targets

      search feed = div class= "x193iq5w x1xwk8fm" role="feed"

      search items = span class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft" text = "Ajouter un(e) ami(e)"
      
      if span with class "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid"

            max page results achieved


      """
      location_selector = "x1y1aw1k x1sxyh0 xwib8y2 xurb0ha"

      page.goto("https://web.facebook.com/search/people?q=aws&filters=eyJjaXR5OjAiOiJ7XCJuYW1lXCI6XCJ1c2Vyc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTEwNzc0MjQ1NjE2NTI1XCJ9In0%3D")
      page.query_selector("div[role='feed']").click()
      print("div clicked")
      page.mouse.wheel(0,99999)
      print("SCROLLING")
      time.sleep(5)
      page.mouse.wheel(0,99999)
      print("SCROLLING")
      time.sleep(5)
      #Go to Personnes

      #Apply a Search term in Ville "Paris"

      