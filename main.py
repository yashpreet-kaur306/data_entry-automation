import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

GOOGLE_FORM = "https://forms.gle/qJNEgqjKHB8bVn6p9"
ZILLOW_LINK = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(url=ZILLOW_LINK)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Webscrapping
soup = BeautifulSoup(response.text, "html.parser")
prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
prices_list = []
for price in prices:
    cost = price.getText().split("+")[0].split("/")[0]
    prices_list.append(cost)
# print(prices_list)

addresses = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
address_list = [address.getText().replace("|", "").strip() for address in addresses]
# print(address_list)

links = soup.find_all("a", class_="property-card-link")
links_list = [link.get("href") for link in links]
# print(links_list)

# Automation
for n in range(len(links_list)):
    driver.get(GOOGLE_FORM)
    time.sleep(3.3)
    address_fill = driver.find_element(by=By.XPATH,
                                       value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_fill.send_keys(address_list[n])

    price_fill = driver.find_element(by=By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_fill.send_keys(prices_list[n])

    link_fill = driver.find_element(by=By.XPATH,
                                    value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_fill.send_keys(links_list[n])
    submit = driver.find_element(By.XPATH,
                                 value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
driver.quit()

