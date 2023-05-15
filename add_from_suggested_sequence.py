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
config = configparser.RawConfigParser()
config.read("config.ini")

#INITIALS
#CONFIG PARSER INIT

SUGGESTED_URL = "https://www.facebook.com/friends/suggestions"
DELAY_RANGE = [30,90]
DELAY_ON_ERROR = 30 # delay in seconds when an error occurs

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
      
            
            page.goto(SUGGESTED_URL,timeout=0)
            time.sleep(10)
            page.query_selector("div[class='x135pmgq']").click()
            
            main_div = page.query_selector("div[class='x135pmgq']")
            
            current_suggested_friends = main_div.query_selector_all("a[class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']")
            # xpath = a[class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']
            # new class = x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid
            # old class = x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid
            while len(current_suggested_friends) <= SEARCH_QUOTA:
                  page.mouse.wheel(0,99999)
                  print("SCROLLING")
                  time.sleep(5)
                  current_suggested_friends = main_div.query_selector_all("a[class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq']")
            print("End of results page found")
            print("Adding results as friends")
            page.wait_for_load_state()


            html = page.content()
            soup = BeautifulSoup(html,"html.parser")

            
            #Go to Personnes
            for account in current_suggested_friends:
                  
                  if "Ajouter comme ami(e)" in account.text_content():
                        
                        print(f"Click the account with details\n {account.text_content()}")
                        if account.query_selector('span:text("Ajouter comme ami(e)")'):
                              account.query_selector('span:text("Ajouter comme ami(e)")').click()
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
                                    

