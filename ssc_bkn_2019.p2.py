"""
Created on Mon Dec 16 00:54:05 2019
@author: akirawisnu
"""
# use this command before starting console
# chromedriver --url-base=/wd/hub

import pandas as pd
import os
#Selenium Party
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

link = "https://sscndata.bkn.go.id/spf"
path = "/home/akirawisnu/Documents/work/pypy/python-learn/SSC_BKN"

os.chdir(path)

driver = webdriver.Chrome()
driver.get(link)

driver.find_element_by_xpath('//*[@id="spf_length"]/label/select/option[4]').click()
sleep(2)

sscbkn=[]
wait = WebDriverWait(driver,10)
# click until next ended
while True:
    table = driver.find_element_by_xpath('//*[@id="spf_wrapper"]')
    table_html = table.get_attribute('innerHTML')
    df = pd.read_html(table_html, "r", encoding="UTF-8")
    df = pd.concat(df)
    sscbkn.append(df)

    #getting next page
    next_page_btn = driver.find_elements_by_xpath('//*[@id="spf_next"]')
    if len(next_page_btn) < 1:
        print("No more pages left")
        break    
    else:
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Next'))).click()
        sleep(1)

sscbkn=pd.concat(sscbkn)
sscbkn.to_stata("ssc_bkn_2019.dta", version=117)

driver.close()
