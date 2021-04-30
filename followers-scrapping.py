import os
import time
import csv

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


print("Enter Credentials ::")
userName = input("Enter User Name:")
passWord = input("Enter Password:")

USER_NAME = userName
PASSWORD = passWord  

followers_list = []

print("Intializing..")
# Open Google Chrome Web Browswer
driver = webdriver.Chrome(
    os.path.dirname(os.path.abspath(__file__))+'\\chromedriver_win32\\chromedriver.exe')


print("Loading site..")
# Get/Open the Site link
driver.get("https://www.instagram.com/")

# Select UserName Element(Text Box)
# WebDriverWait : (Load the site on Driver Variable, Time out Seconds)
# By.CSS_SELECTOR : Select Element by CSS Name
username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

# clear username and password before entering the inputs
username.clear()
password.clear()

print("Auto Entering Credentials..")
# Entering username and password
username.send_keys(USER_NAME)
password.send_keys(PASSWORD)

# LogIn Button
loginBtn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# Click not Now Button
not_now = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

# Not Now for Notifications
not_now2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

print("Load the Acoount Page..")
# Load the Account Page
driver.get("https://www.instagram.com/{0}/".format(USER_NAME))

print("Open followers..")
# Click the 'followers' link
follower_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'followers')]"))).click()

#scroll Whole Window
driver.execute_script("window.scrollTo(0, 4000);")

#Locating all Span elements that contains Name List
following_elems = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH,"//span[contains(@class,'Jv7Aj mArmR MqpiF ')]")))
print(following_elems)


print("Gathering the data...")
#find all li elements in list and scroll it
popupbody = driver.find_element_by_xpath("//div[@class='isgrP']")
scroll = 0
#scroll 26 times
while scroll < 26:
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', popupbody)
    time.sleep(2)
    scroll += 1
    
fList  = driver.find_elements_by_xpath("//div[@class='isgrP']//li")

#Getting Name List from Followers popup
for name in driver.find_elements_by_css_selector('a'):
    namelist = name.text
    followers_list.append(namelist)

#Remove null Values from List
while "" in followers_list:
    followers_list.remove("")


print("--------- Collected Data ----------------------------------------------")
print(followers_list)
print("-------------------------------------------------------")
print("Total Collected Data: {}".format(len(fList)))

#Make/Edit CSV File 
with open(os.path.dirname(os.path.abspath(__file__))+'\\nameList.csv', 'w', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter="\n")
    writer.writerow(followers_list)
    
print("File Created.")
print("Process Done.")

while(True):
    pass
