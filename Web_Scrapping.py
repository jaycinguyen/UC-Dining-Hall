from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def Web_scrape(url_link):
    # Use webdriver-manager to automatically handle the chromedriver
    service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()

    # Add the headless option to run Chrome in the background
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU usage (often necessary for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Ensure it runs on a server without sandboxing

    # Launch the browser
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target URL
        browser.get(url_link)

        # Wait for the main content to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))


        # Get the page source
        page_source = browser.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
    finally:
        # Ensure the browser is always closed
        browser.quit()

    return soup

### GET THE NAME AND STATUS AND TIME OF DINING HALL ###
link_1 = "https://ucdining.sodexomyway.com/en-us/locations/"  # Replace with your target URL
soup_1 = Web_scrape(link_1)

# Find all 'h2' tags
#test = soup_1.find_all('h2') #=> Will appear the title "Location" and the contact information at the bottom the page
#print(test)

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


# for status, time, dining_name in zip(status_list, time_list, dining_name_list):
#      if status == "Open":
#          print(f'{dining_name} is {status}, {time}')
#      if status == "Closed":
#          print(f'{dining_name} is {status}')

### GET EACH PRIVATE WEBSITE OF DINING HALLS ###

dining_full_url_list=[]
dining_w_menu_list=[]

base_url = "https://ucdining.sodexomyway.com"  # The base URL for your site

dining_link_tags = soup_1.find_all('div', class_='Locationstyles__LocationComponent-sc-3mxfm6-4')

for dining_link in dining_link_tags:
    link = dining_link.a
    if link and 'href' in link.attrs:
        full_url = base_url + link['href']
        dining_full_url_list.append(full_url)
        #print(link['href'])
        #print(full_url)
    menu_link = dining_link.find('div',class_='menu-link')
    if menu_link:
        dining_w_menu_list.append(full_url)

#print(dining_full_url_list)
#print(dining_w_menu_list)

### SCRAPE DATA FROM EACH DINING HALLS' LINK ###

for l in dining_w_menu_list:
     print(f"Processing: {l}")
     soup_2 = Web_scrape(l)
     headers = soup_2.find_all('h2',tabindex="0")  # Match <h2> tags with `tabindex="0"`
     print(headers)
     for header in headers:
        print(header)  # Print the menu category (e.g., "BREAKFAST")