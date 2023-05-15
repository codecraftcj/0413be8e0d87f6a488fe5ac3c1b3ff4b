"""
    A Bot to automatically add nearby friends in the background on facebook
    #random hash: 0413be8e0d87f6a488fe5ac3c1b3ff4b
"""
import configparser
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import random
import string
import time

#INITIALS
#CONFIG PARSER INIT
config = configparser.RawConfigParser()
config.read("config.ini")

SEARCH_SEQUENCE_URL_LIST = [
      "https://web.facebook.com/search/people?q=pes&filters=eyJjaXR5OjAiOiJ7XCJuYW1lXCI6XCJ1c2Vyc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTEwNzc0MjQ1NjE2NTI1XCJ9In0%3D",

]
DELAY_RANGE = [30,90]
DELAY_ON_ERROR = 30 # delay in seconds when an error occurs
SEARCH_QUOTA = 50
BROWSER_IS_HEADLESS = False
SEARCH_QUOTA = config.get("Facebook Account","SEARCH_QUOTA")
BROWSER_IS_HEADLESS = config.get("Facebook Account","BROWSER_IS_VISIBLE")
USERNAME = config.get("Facebook Account","USERNAME")
PASSWORD = config.get("Facebook Account","PASSWORD")

current_added_friends = []

def random_delay(numbers):
    """Generate a random delay in seconds within the range defined by a list of two numbers."""
    start = numbers[0]
    end = numbers[1]
    delay = random.uniform(start, end)
    time.sleep(delay)

def get_3_characters():
    """Generate a random 3 character string of lowercase letters."""
    return ''.join(random.choices(string.ascii_lowercase, k=3))

def search_url_modifier(url):

      query_string = url.split("q=")[1].split("&")[0]
      new_url = url.replace(query_string,get_3_characters())

      return new_url

                   


with sync_playwright() as playwright:

      #BOT LOGIN
      chromium = playwright.chromium # or "firefox" or "webkit".
      browser = chromium.launch(headless=BROWSER_IS_HEADLESS) #switch to False when debugging
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
      # elements = page.query_selector_all("span:text('Ajouter')")
      # for element in elements:
      #       print(element.text_content())

      #ADD SEARCH QUERY
      
      #Search in facebook a random string

      while len(current_added_friends) <= SEARCH_QUOTA: 
      
            new_query = search_url_modifier(SEARCH_SEQUENCE_URL_LIST[0])
            page.goto(new_query,timeout=0)
            page.query_selector("div[role='feed']").click()
            print("div clicked")

            # new class = x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid
            # old class = x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid
            while page.query_selector("span[class='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid']") == None:
                  page.mouse.wheel(0,99999)
                  print("SCROLLING")
                  time.sleep(5)
            print("End of results page found")
            print("Adding results as friends")
            page.wait_for_load_state()


            html = page.content()
            soup = BeautifulSoup(html,"html.parser")

            accounts_on_feed = page.query_selector("div[role='feed']").query_selector_all("div[class='x1yztbdb']")
            #Go to Personnes
            for account in accounts_on_feed:
                  
                  if "Ajouter un(e) ami(e)" in account.text_content():
                        
                        print(f"Click the account with details\n {account.text_content()}")
                        if account.query_selector('span:text("Ajouter un(e) ami(e)")'):
                              account.query_selector('span:text("Ajouter un(e) ami(e)")').click()
                              current_added_friends.append(account)
                              random_delay(DELAY_RANGE)
                              additional_delay = 0

                              error_modal = page.query_selector("div[class='x1jx94hy xh8yej3 x1hlgzme xvcs8rp x1bpvpm7 xefnots x13xjmei x1n2onr6 xv7j57z']")
                        
                              while error_modal != None:
                                    additional_delay+=1
                                    error_button = error_modal.query_selector("div[class='x1n2onr6 x1ja2u2z x78zum5 x2lah0s xl56j7k x6s0dn4 xozqiw3 x1q0g3np xi112ho x17zwfj4 x585lrc x1403ito x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xbxaen2 x1u72gb5 xtvsq51 x1r1pt67']")
                                    error_button.click()

                                    print(f"Error found trying again in {DELAY_ON_ERROR+additional_delay}")
                                    time.sleep(DELAY_ON_ERROR+additional_delay)

                                    # account.query_selector('span:text("Ajouter un(e) ami(e)")').click()
                                    error_modal = page.query_selector("div[class='x1jx94hy xh8yej3 x1hlgzme xvcs8rp x1bpvpm7 xefnots x13xjmei x1n2onr6 xv7j57z']")
      browser.close()
                                    

