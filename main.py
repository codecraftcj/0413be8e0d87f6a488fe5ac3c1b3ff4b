import pandas as pd
import numpy as np
import random
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import random
import string
import time
import subprocess
import configparser

ADD_FRIENDS = True
GET_NOTIFICATIONS = True
CMD = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

#get dfs
excel_file = "settings.xlsx"
accounts_df = pd.read_excel(excel_file,sheet_name="Accounts",engine="openpyxl")
search_names_df = pd.read_excel(excel_file,sheet_name="Search Names",engine="openpyxl")
search_names_list = search_names_df["Search Names"].to_list()
excel_writer = pd.ExcelWriter(excel_file,engine="openpyxl")
accounts_df.to_excel(excel_writer,sheet_name="Accounts",index=False)
search_names_df.to_excel(excel_writer,sheet_name="Search Names",index=False)
excel_writer.close()

num_names_to_drop = 3  # Specify the number of names to search to drop


def search_url_modifier(url,name):

      query_string = url.split("q=")[1].split("&")[0]
      new_url = url.replace(query_string,name)

      return new_url

def notify(title, text):
      if GET_NOTIFICATIONS:
            subprocess.call(['osascript', '-e', CMD, title, text])

if __name__ == "__main__":
    with sync_playwright() as playwright:

        #BOT LOGIN
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=False) #switch to False when debugging
            
        for index,account in accounts_df.iterrows():
            if account["FB_ADDER_STATUS"] != "Complete" and account["FB_ADDER_STATUS"] != "Warned":
                account_context = browser.new_context()
                account_page = account_context.new_page()
                account_page.goto("https://www.facebook.com/")
                time.sleep(5)
                
                if account_page.query_selector("//*[text() = 'Allow all cookies']") is not None:
                    account_page.query_selector("//*[text() = 'Allow all cookies']").click()
                    time.sleep(2)

                account_page.query_selector("input[id='email']").click()
                account_page.keyboard.type(account["Profil"])
                account_page.query_selector("input[id='pass']").click()
                account_page.keyboard.type(account["MDP à jour"])
                account_page.query_selector("button[type='submit']").click()

                time.sleep(10)

                current_added_friends = []
                chosen_names = []
                current_names = search_names_list
                current_account_warned = False
                while len(chosen_names) < num_names_to_drop and search_names_list:
                    name_index = random.randint(0, len(search_names_list) - 1)
                    popped_name = search_names_list.pop(name_index)
                    chosen_names.append(popped_name)
                

                for search_name in chosen_names:
                    if len(current_added_friends) < int(account["amis"]) and not current_account_warned:
                        new_search_url = search_url_modifier(account["REGION"],search_name)
                    
                        account_page.goto(new_search_url,timeout=0)
                        time.sleep(5)
                        account_page.query_selector("div[role='feed']").click()
                        print("div clicked")

                        # new class = x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid
                        # old class = x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa x2b8uid
                        accounts_on_feed = account_page.query_selector("div[role='feed']").query_selector_all("div[class='x1yztbdb']")
                        #text = Fin des résultats
                        while account_page.query_selector("//*[text() = 'Fin des résultats']") is not None or len(accounts_on_feed) < int(account["amis"]) :
                            
                            accounts_on_feed = account_page.query_selector("div[role='feed']").query_selector_all("div[class='x1yztbdb']")
                            account_page.mouse.wheel(0,99999)
                            print("SCROLLING")
                            time.sleep(1)
                        print("End of results page found")
                        print("Adding results as friends")
                        account_page.wait_for_load_state()

                        html = account_page.content()
                        soup = BeautifulSoup(html,"html.parser")

                        accounts_on_feed = account_page.query_selector("div[role='feed']").query_selector_all("div[class='x1yztbdb']")
                        added_friends_count = 0
                        if len(accounts_on_feed) > 0:
            
                            print("Adding friends found")
                            #Go to Personnes
                            for friend in accounts_on_feed:
                                    
                                    if "Ajouter un(e) ami(e)" in friend.text_content():
                                        
                                        if friend.query_selector('span:text("Ajouter un(e) ami(e)")'):
                                            
                                            if ADD_FRIENDS:
                                                friend.query_selector('span:text("Ajouter un(e) ami(e)")').click()
                                                
                                                added_friends_count+=1
                                                current_added_friends.append(friend)
                                                
                                                print(f"Clicked the account with details\n {friend.text_content()}")
                                                print(f"Added {len(current_added_friends)}/{account['amis']} for {account['Account Name']}")
                                                
                                                
                                                if len(current_added_friends) == int(account['amis']):
                                                    break

                                                time.sleep(2)
                                        
                                                if account_page.query_selector("//*[text() = 'Impossible d’envoyer l’invitation']"):
                                                    notify("Facebook Friend Adder",f"Account {account['Account Name']} Warned moving over to the next account")
                                                    time.sleep(3)
                                                    print("Can't send anymore requests")

                                                    accounts_df.at[index,"FB_ADDER_STATUS"] = "Warned"
                                                    current_account_warned = True
                                                    excel_writer = pd.ExcelWriter(excel_file,engine="openpyxl")
                                                    accounts_df.to_excel(excel_writer,sheet_name="Accounts",index=False)
                                                    search_names_df.to_excel(excel_writer,sheet_name="Search Names",index=False)
                                                    excel_writer.close()
                                                    account_page.close()
                                                    break
                                                
                                                if account_page.query_selector("//*[text() = 'OK']"):
                                                    account_page.query_selector("//*[text() = 'OK']").click()
                                                    time.sleep(2)

                                                accounts_df.at[index,"FRIENDS_ADDED"] = len(current_added_friends)
                                                excel_writer = pd.ExcelWriter(excel_file,engine="openpyxl")
                                                accounts_df.to_excel(excel_writer,sheet_name="Accounts",index=False)
                                                search_names_df.to_excel(excel_writer,sheet_name="Search Names",index=False)
                                                excel_writer.close()

                                                
                            notify("Facebook Friend Adder",f"Added {len(current_added_friends)} for {account['Account Name']} at search URL :{new_search_url}")
                            time.sleep(3)
                        else:
                            notify("Facebook Friend Adder",f"Can't find any friends for {account['Account Name']} at search URL :{new_search_url}")
                            print(f"Can't find any friends for {account['Account Name']} at search URL :{new_search_url}")
                            time.sleep(3)
                    else:
                        if current_account_warned:
                            notify("Facebook Friend Adder",f"Can't add friends for {account['Account Name']} Account is Flagged")
                            time.sleep(3)
                        else: 
                            print(f"All done for {account['Account Name']} skipping {search_name}")

                account_page.close()
                accounts_df.at[index,"FB_ADDER_STATUS"] = "Complete"
                excel_writer = pd.ExcelWriter(excel_file,engine="openpyxl")
                accounts_df.to_excel(excel_writer,sheet_name="Accounts",index=False)
                search_names_df.to_excel(excel_writer,sheet_name="Search Names",index=False)
                excel_writer.close()
                notify("Facebook Friend Adder","Done Running!")
                
        print("No Accounts available to automate")
        print("Exiting in 10 seconds")
        time.sleep(10)

            

                
        

        