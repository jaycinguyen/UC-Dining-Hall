from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def Web_scrap(url_link):
    # Use webdriver-manager to automatically handle the chromedriver
    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()

    # Add the headless option to run Chrome in the background
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU usage (often necessary for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Ensure it runs on a server without sandboxing

    # Launch the browser
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # Open the page you want to scrape
    browser.get(url_link)  # Replace with your target URL

    # Get the page source
    page_source = browser.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    # Close the browser when done
    browser.quit()

    return soup

link_1 = "https://ucdining.sodexomyway.com/en-us/locations/"  # Replace with your target URL
soup_1 = Web_scrap(link_1)

# Find all 'h2' tags
test = soup_1.find_all('h2') #=> Will appear the title "Location" and the contact information at the bottom the page

status_list = []
time_list = []
dining_name_list = []

status_tags = soup_1.find_all('div', class_ = 'OpenChipstyles__Wrapper-sc-1vubns5-0 fyYRFO')
#print(status)
for s in status_tags:
    sta = s.find_all('div',class_= 'text')
    for m in sta:
        status = m.text
        status_list.append(status)
        # print(status)

dining_name_tags = soup_1.find_all('div',class_= 'location-description-container')
for dining in dining_name_tags:
    dining_name = dining.h2.text
    dining_name_list.append(dining_name)
    #print(dining_name)
    time_tag = dining.find_all('div',class_= 'text')
    for t in time_tag:
        time = t.text
        time_list.append(time)
        #print(f'Time: {time}') #This will be updated following the website

#print(status_list)
#print(time_list)
#print(dining_name_list)

for status, time, dining_name in zip(status_list, time_list, dining_name_list):
     if status == "Open":
         print(f'{dining_name} is {status}, {time}')
     if status == "Closed":
         print(f'{dining_name} is {status}')
