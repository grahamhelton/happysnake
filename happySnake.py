#! /usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.select import Select
from colorama import init, Fore, Style
import json
import time
import sys
#Initialize variables and get config
with open('../config.json') as configFile:
    data=json.load(configFile)
cardData =  data["cardNumber"]
expoData =  data["expo"]
dic = {}
count = 0
options = FirefoxOptions()
nameList = []
priceList = []
reset = Style.RESET_ALL
tick = Fore.BLUE + "[" + Fore.GREEN + "+" + Fore.BLUE + "]" + reset

print(Fore.GREEN +
'''
       (  )   (   )  )
        ) (   )  (  (
        ( )  (    ) )
        _____________
       <_____________> ___
       |             |/ _ \\
       |   O    O      | | |
       |     <         |_| |
    ___|   \____/    |\___/
   /    \___________/    \\
   \_____________________/
--- H A P P Y    S N A K E ---
''' + reset
)
def goToParent():
    driver.switch_to.parent_frame();

if "-s" in sys.argv:
    options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.get("https://happymugcoffee.com/collections/roasted-coffee")

# List the coffee names on the site
print(tick +  " Which coffee would you like? " + reset)
blends = driver.find_element_by_id("Collection")
#print(blends.text)
blendName = driver.find_elements_by_class_name("visually-hidden")
blendPrice = driver.find_elements_by_class_name("price")

#Append names and prices to list
for name in blendName:
    nameList.append(name.text)
for price in blendPrice:
    priceList.append(price.text)

# Clean up list due to oddly formatted website
nameFixed = []
for i in nameList:
    if i not in nameFixed:
        nameFixed.append(i)
del nameFixed[0:3]
del nameFixed[-1]
nameFixed.remove("Regular price")
nameFixed.remove("Coffee Subscription - Roaster's Choice A")
nameFixed.remove("Coffee Subscription - Roaster's Choice B")

# Assign coffee names to key/value pair and print them for the user
for i in nameFixed:
    count+=1
    dic[count]=i
for key, value in dic.items():
    print(key, ' : ', value)
selection = input(tick + Fore.BLUE + " Type the number of the coffee you would like\n" + reset)

# Lookup the key/value in dictionary then click the correct coffee
value = dic[int(selection)]
print(tick + Fore.BLUE + " Selecting " + value + "...")
driver.find_element_by_link_text(value).click()
cart = driver.find_elements_by_id("AddToCart-product-template")[0]
cart.click()
driver.find_element_by_xpath("/html/body/div[4]/main/div/div/form/div/div/div[2]/div[4]/input[2]").click()

# Input shipping info (Condense into for loop later)
print(tick + Fore.BLUE + " Adding info from " + Fore.GREEN + "config.json" + Fore.BLUE + "..." + reset)
time.sleep(2)
send = driver.find_element_by_id("checkout_email")
send.send_keys(data["email"])
send = driver.find_element_by_id("checkout_shipping_address_first_name")
send.send_keys(data["firstName"])
send = driver.find_element_by_id("checkout_shipping_address_last_name")
send.send_keys(data["lastName"])
send = driver.find_element_by_id("checkout_shipping_address_address1")
send.send_keys(data["address"])
send = driver.find_element_by_id("checkout_shipping_address_address2")
send.send_keys(data["apartment"])
send = driver.find_element_by_id("checkout_shipping_address_city")
send.send_keys(data["city"])
send = driver.find_element_by_id("checkout_shipping_address_zip")
send.send_keys(data["zip"])

#Continue to shipping and wait for load
driver.find_element_by_id("continue_button").click()
time.sleep(2)
driver.find_element_by_id("continue_button").click()
time.sleep(2)

#Switch to iframe and add card data
iframe = driver.find_element_by_xpath("//iframe[@class='card-fields-iframe']")
driver.switch_to.frame(iframe)
send = driver.find_element_by_xpath("//*[@id='number']")

# Add numbers one by one becuase it doesn't like when you add it all at once
for i in range (0,len(cardData)):
    send.send_keys(cardData[i])

# Input firstName and firstName
goToParent()
driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-name-')]"))
driver.find_element_by_id("name").send_keys(data["firstName"])
driver.find_element_by_id("name").send_keys(" " + data["lastName"])

# Input expiration date
goToParent()
driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-expiry-')]"))
for i in range(0,len(expoData)):
    driver.find_element_by_id("expiry").send_keys(expoData[i])

# Input CVC
goToParent()
driver.switch_to.frame(driver.find_element_by_xpath("//*[contains(@id, 'card-fields-verification_value-')]"))
driver.find_element_by_id("verification_value").send_keys(data["cvc"])

# Press pay
goToParent()
total = driver.find_element_by_xpath("/html/body/div/div/aside/div[2]/div[1]/div/div[3]/table/tfoot/tr/td/span[2]").text
pay = input(tick + Fore.BLUE + "Your total is: " + Fore.GREEN + total + Fore.RED+ "\nSubmit order? Yes/No: " + reset)
# Pay now
if "y" in pay:
    print(tick + Fore.GREEN + "Processing transaction... (this will take 10 seconds)")
    time.sleep(10)
    print(tick + Fore.GREEN + "Your coffee has been bought!")
   #UNCOMMENT THIS WITH CARE, IT WILL PROCESS YOUR ORDER
   #driver.find_element_by_id('continue_button').click()
else:
    print(Fore.RED + "Exiting without buying!")

driver.close()
