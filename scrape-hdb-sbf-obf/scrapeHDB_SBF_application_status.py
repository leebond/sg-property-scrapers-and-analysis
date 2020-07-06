# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 18:01:16 2019

@author: david
"""

import re, os
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
driver = webdriver.Chrome("C:/Users/guanhua/Documents/chromedriver/chromedriver.exe")
http = "https://services2.hdb.gov.sg/webapp/BP13BTOENQWeb/AR_Nov2019_SBF?strSystem=SBF"
driver.get(http)

def processRowData(rowdata, ncells):
    try:
        data = rowdata.split()
        print(data)
        if len(ncells) == 7:
            return data[0], data[1:]
        elif len(ncells) == 6:
            return None, data[0:]
    except:
        return None, None

secondTable_title = driver.find_element_by_xpath('//*[@id="print"]/div[5]/div/h5')
secondTable_title_text = secondTable_title.text
secondTable = driver.find_element_by_xpath('//*[@id="print"]/div[6]/div/div/div/div/div/div/div/table')
rows = secondTable.find_elements_by_tag_name('tr')
print(len(rows))

df = pd.DataFrame(columns = ['Estate', 'Flat Type', 'No of Units', 'Number of Applicants', 'First Timers Application Rate', \
                             'Second Timers Application Rate', 'Overall Timers Application Rate'])

estate = None
for i in range(2, len(rows) - 3):
    rowXpath = '//*[@id="print"]/div[6]/div/div/div/div/div/div/div/table/tbody/tr[' + str(i) + ']'
    row = driver.find_element_by_xpath(rowXpath)
    rowdata = row.find_elements_by_tag_name('td')
    out = [data.text for data in rowdata]
    if len(out) == 7:
        estate = out[0]
        df = df.append({'Estate': out[0], 'Flat Type': out[1], 'No of Units': out[2], 'Number of Applicants': out[3], \
                        'First Timers Application Rate': out[4], 'Second Timers Application Rate': out[5], 'Overall Timers Application Rate': out[6]}, ignore_index=True)
    elif len(out) == 6:
        df = df.append({'Estate': estate, 'Flat Type': out[0], 'No of Units': out[1], 'Number of Applicants': out[2], \
                        'First Timers Application Rate': out[3], 'Second Timers Application Rate': out[4], 'Overall Timers Application Rate': out[5]}, ignore_index=True)

#print(df.shape)
#print(df)

if not os.path.exists('./data'):
    os.makedirs('./data')

df.to_csv(f"./data/hdb_sbf_application_status-{secondTable_title_text}.csv", index = False)