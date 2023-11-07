import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
# google search web scraping
start = time.time()
search_engine = "https://google.com/search?q="

query = "apples"

search = search_engine + query # the search url

options = webdriver.ChromeOptions()

options.add_argument('--headless')


driver = webdriver.Chrome(options=options)


driver.get(search)

page = driver.page_source







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


# attempting to find the links of all the google recommeneded pages
for result in web_results.find_all("div", class_="MjjYud"):
  try:
      melink = result.find('a', href=True)
      link = melink['href']
      print(link)
      print('\n')
  except TypeError:
     print("Must not have a link")
  #print(type(result), type(melink))

#result = web_results.find("div", class_="MjjYud")

et = time.time()

print((et - start), "seconds")