# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:23:08 2020

@author: guanhua
"""


import re, os
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
from datetime import datetime
from urllib.parse import unquote_plus
from tqdm import tqdm


def clickBuyerOption(buyer_button_xpath):
    # buyer_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, buyer_button_xpath)))
    buyer_button = driver.find_element_by_xpath(buyer_button_xpath)
    radio_label_xpath = '//*[@id="frmRTIS"]/div[1]/div/div[1]/div[3]/div[2]/label[2]'
    radio_label = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, radio_label_xpath)))
    if buyer_button:
        driver.execute_script('arguments[0].click();', buyer_button)
        # print(radio_label.text)

def getOptions(xpath):
    # elem = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elem = driver.find_element_by_xpath(xpath)
    if elem:
        all_options = elem.find_elements_by_tag_name("option")
        options_values = [option.get_attribute("value") for option in all_options if option.get_attribute("value") != '']
        # print(options_values)
        return options_values


def getSelector(xpath):
    elem = driver.find_element_by_xpath(xpath)
    if elem:
        return Select(elem)

# def cleanSqm(sqm_text):
#     sqm_num = re.findall('\d+.\d+',sqm_text)[0]
#     sqm_desc = re.findall('[A-Za-z]+',sqm_text)[0]
#     return sqm_num, sqm_desc

def getFloorArea(sqm_text):
    sqm_num = re.findall('\d+.\d+',sqm_text)[0]
    return sqm_num

def getFlatModel(sqm_text):
    sqm_desc = re.findall('[A-Za-z]+',sqm_text)[0]
    return sqm_desc

def cleanTown(town_text):
    town_list = town_text.split()
    town_code = town_list[0]
    town_name = ' '.join(town_list[1:])
    return town_code, town_name

def getTownResaleDetails(town, flat_type):
    
    flat_type_dic = {'01':'1-Room','02':'2-Room','03':'3-Room','04':'4-Room','05':'5-Room','06':'Executive','08':'Multi-Generation'}
    
    main = f'//*[@id="divLargeDetail2"]/div/div[3]/table'
    project_tbl = driver.find_element_by_xpath(main).get_attribute('outerHTML')
    tbl_data = pd.read_html(project_tbl)[0]
    
    tbl_data.columns = ['Block','Street','Storey','Floor Area/Flat Model','Lease Commencement Date','Remaining Lease','Price','Resale Registration Date']
    
    tbl_data['Floor Area'] = tbl_data['Floor Area/Flat Model'].apply(getFloorArea)
    tbl_data['Flat Model']= tbl_data['Floor Area/Flat Model'].apply(getFlatModel)
    tbl_data['Flat Type'] = flat_type
    tbl_data = tbl_data.replace({'Flat Type': flat_type_dic})
    
    town_code, town_name = cleanTown(town)   
    tbl_data['Town'] = town_name
    tbl_data['Town Code'] = town_code
    
    tbl_data['Resale Registration Month']= tbl_data['Resale Registration Date'].apply(lambda x: x[:3])
    tbl_data['Resale Registration Year']= tbl_data['Resale Registration Date'].apply(lambda x: x[-4:])
    
    tbl_data = tbl_data[['Town Code','Town','Block','Street','Storey','Floor Area/Flat Model','Floor Area','Flat Model','Flat Type',\
                         'Lease Commencement Date','Remaining Lease','Price','Resale Registration Date','Resale Registration Month',\
                             'Resale Registration Year']]
    
    return tbl_data

def clickNewEnquiry():
    cnt = 0
    while cnt < 3:
        try:
            new_xpath = '/html/body/form[1]/div[5]/div/a'
            # new_enquiry_btn = driver.find_element_by_xpath(new_xpath)
            new_enquiry_btn = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, new_xpath)))
            new_enquiry_btn.click()
        except TimeoutException:
            cnt += 1

if __name__=='__main__':
    driver = webdriver.Chrome("C:/Users/guanhua/Documents/chromedriver/chromedriver.exe")
    http = 'https://services2.hdb.gov.sg/webapp/BB33RTIS/BB33SSearchWidget'   
    driver.get(http)
    
    buyer_button_xpath = '/html/body/form[1]/div[1]/div/div[1]/div[3]/div[2]/label[2]/input'
    flat_type_xpath = '//*[@id="frmRTIS"]/div[1]/div/div[1]/div[4]/div[2]/select'
    hdb_town_xpath = '//*[@id="id_t"]'
    last_date_xpath = '//*[@id="dteRange"]'
    flat_type_options_values = getOptions(flat_type_xpath)
    hdb_town_options_values = getOptions(hdb_town_xpath)
    last_date_options_values = getOptions(last_date_xpath)
    
    flat_type_options_selector = getSelector(flat_type_xpath)
    hdb_town_options_selector = getSelector(hdb_town_xpath)
    last_date_options_selector = getSelector(last_date_xpath)

    # print(flat_type_options_values, hdb_town_options_values)
    flat_type_options_selector.select_by_value('01')
    hdb_town_options_selector.select_by_value('AMK     Ang Mo Kio')
    last_date_options_selector.select_by_value('12')
    submit_btn_xpath = '/html/body/form[1]/div[3]/div[1]/a'
    submit_btn = driver.find_element_by_xpath(submit_btn_xpath)
    submit_btn.click()
    
    df = pd.DataFrame()
    
    for hdb_town in hdb_town_options_values:
        for flat_type in flat_type_options_values:
    
            try:
                form_xpath = '//*[@id="frmRTIS"]'
                form_element = driver.find_element_by_xpath(form_xpath)
                if form_element:
                    print(flat_type, hdb_town)
                    flat_type_options_selector = getSelector(flat_type_xpath)
                    hdb_town_options_selector = getSelector(hdb_town_xpath)
                    last_date_options_selector = getSelector(last_date_xpath)
                    
                    clickBuyerOption(buyer_button_xpath)
                    flat_type_options_selector.select_by_value(flat_type) #('04')
                    hdb_town_options_selector.select_by_value(hdb_town) #('QT      Queenstown')select_by_value
                    last_date_options_selector.select_by_value('12')
            
                    # driver.implicitly_wait(100)
                    submit_btn_xpath = '/html/body/form[1]/div[3]/div[1]/a'
                    # submit_btn = driver.find_element_by_xpath(submit_btn_xpath)
                    submit_btn = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, submit_btn_xpath)))

                    if submit_btn:
                        # print(submit_btn.is_enabled())
                        submit_btn.click()

                        try:
                            table_xpath = '//*[@id="divLargeDetail2"]/div/div[3]/table'
                            resale_table = driver.find_element_by_xpath(table_xpath)
                            # resale_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, table_xpath)))
                            if resale_table:
                                print('Resale Table Details Present')
                                resale_details_table_xpath = '//*[@id="divLargeDetail2"]/div/div[3]/table/tbody/tr[*]'
                                resale_details_table_rows = driver.find_elements_by_xpath(resale_details_table_xpath)
                                print(f'{len(resale_details_table_rows)} transactions found' )
                                                               
                                data_df = getTownResaleDetails(hdb_town, flat_type)
                                df = df.append(data_df)
                                
                                if not os.path.exists('output'):
                                    os.makedirs('output')
                                df.to_excel(f"./output/HDB_resale_prices_{datetime.now().date()}.xlsx", index=False)
                                
                                print('New Enquiry')
                                new_xpath = '//*[@id="btns"]/div[1]/a'
                                new_enquiry_btn = driver.find_element_by_xpath(new_xpath)
                                new_enquiry_btn.click()
                        
                        except NoSuchElementException:
                            ## click New Enquiry Button
                            clickNewEnquiry()

            except:
                raise
    
    print(df.shape)
    if not os.path.exists('output'):
        os.makedirs('output')
    df.to_excel(f"./output/HDB_resale_prices_{datetime.now().date()}.xlsx", index=False)