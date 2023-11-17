import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
# google search web scraping
start = time.time()
search_engine = "https://google.com/search?q="
# this is what the program will seach up using google
query = input("A random question you can ask the ai: ")

search = search_engine + query # the search url

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# making browser headless


driver = webdriver.Chrome(options=options)
# creating my browsing object

driver.get(search) # loads webpage in headless browser

ini_height = driver.execute_script("return document.body.scrollHeight")
# Scrolls to bottom of page since google adds more when you scroll down
while True:
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
   time.sleep(1)

   new_height = driver.execute_script("return document.body.scrollHeight")

   if new_height == ini_height:
      break
   ini_height = new_height



page = driver.page_source
# retrieving my webpage and getting the html contents





# ignore for now

#search_page = requests.get(search)
#search_page = ''
# manages and limits requests rates.
#while search_page == '':
  #  try:
   #     search_page = requests.get(search)
   #     break
   # except:
   #     print("Connection refused by the server..")
   #     print("Let me sleep for 5 seconds")
    #    print("ZZzzzz...")
    #    time.sleep(5)
    #    print("Was a nice sleep, now let me continue...")
    #    continue







# google page 
web_results = BeautifulSoup(page, "html.parser")

links = 0
# attempting to find the links of all the google recommeneded pages
for result in web_results.find_all("div", class_="MjjYud"):
  try:
      melink = result.find('a', href=True)
      link = melink['href']
      print(link)
      links+=1
      print('\n')
  except TypeError:
     print("Must not have a link")
  #print(type(result), type(melink))"""

#result = web_results.find("div", class_="MjjYud")

et = time.time()
print((et - start), "seconds") # code execution time
print("\n", links, " links") # amount of links