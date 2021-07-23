# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 17:22:13 2020

@author: guanhua
"""


import re, os, sys
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime
from urllib.parse import unquote_plus
from tqdm import tqdm
from glob import glob



def getOptions(xpath):
    # elem = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elem = driver.find_element_by_xpath(xpath)
    if elem:
        all_options = elem.find_elements_by_tag_name("option")
        options_values = [option.get_attribute("value") for option in all_options if option.get_attribute("value") != '']
        # print(options_values)
        return options_values


def getSelector(xpath):
    # elem = driver.find_element_by_xpath(xpath)
    elem = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    if elem:
        return Select(elem)
    else:
        print('Date not selected')


def setDateSelectors():
    date_options_xpath = '/html/body/div/div[4]/div[4]/form/div/div[1]/div[1]/div/div/select[1]'
    date_values = getOptions(date_options_xpath)
    # print(date_values)
    st_date_selector = getSelector(date_options_xpath)
    
    date_options_xpath2 = '/html/body/div/div[4]/div[4]/form/div/div[1]/div[1]/div/div/select[2]'
    end_date_selector = getSelector(date_options_xpath2)
    
    st_date_selector.select_by_value(date_values[-1])
    end_date_selector.select_by_value(date_values[0])


def getTableData():
    try:
        project_tbl_xpath = '/html/body/div/div[4]/form/div[4]/table'
        # project_tbl = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, project_tbl_xpath))).get_attribute('outerHTML')
        project_tbl = driver.find_element_by_xpath(project_tbl_xpath).get_attribute('outerHTML')
        project_tbl_data = pd.read_html(project_tbl)

    except NoSuchElementException:
        project_tbl_xpath = '/html/body/div/div[4]/form/div[4]/div/table'
        # project_tbl = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, project_tbl_xpath))).get_attribute('outerHTML')
        project_tbl = driver.find_element_by_xpath(project_tbl_xpath).get_attribute('outerHTML')
        project_tbl_data = pd.read_html(project_tbl)
            
    return project_tbl_data




if __name__=='__main__':
    if len(sys.argv) < 2:
        print('please provide run type >python this_script.py "new" or "continue"')
        sys.exit(0)
    mode = sys.argv[1]
    print(mode)
    driver = webdriver.Chrome("C:/Users/LEEbo/Documents/chromedriver/chromedriver.exe")
    http = 'https://www.ura.gov.sg/realEstateIIWeb/transaction/search.action'   
    driver.get(http)
    
    df = pd.DataFrame(columns = ['Project Name','Street Name','Type','Postal District','Market Segment','Tenure','Type of Sale'
                                 ,'No. of Units','Price','Nett Price','Area (Sqft)','Type of Area','Floor Level','Unit Price ($psf)'
                                 ,'Date of Sale'])
    
    setDateSelectors()
    
    project_xpath = '/html/body/div/div[4]/div[4]/form/div/div[1]/div[3]/div/div[1]/div/a'
    projects = driver.find_elements_by_xpath(project_xpath)
    projects_names = [p.text for p in projects]
    print(len(projects))
    
    if not os.path.exists('output'):
        os.makedirs('output')


    if mode == 'new':
        start_count = 0
        saved_projects = ['new']
    elif mode == 'continue':
        # print(projects_names)
        output_filepath = './output/Private_*.xlsx'
        files = glob(output_filepath)
        latest_file = files[-1]
        print(latest_file)
        saved_df = pd.read_excel(latest_file)
        saved_projects = saved_df['Project Name'].unique().tolist()
        last_saved_project = saved_projects[-1]
        print(last_saved_project)
        print(len(saved_projects))
        start_count = projects_names.index(last_saved_project)
    
    for i in tqdm(range(start_count, len(projects))):
        # first_project = projects[0]
        # first_project.click()
        setDateSelectors()
        project_xpath = '/html/body/div/div[4]/div[4]/form/div/div[1]/div[3]/div/div[1]/div/a'
        projects = driver.find_elements_by_xpath(project_xpath)
        
        
        print(i, projects[i].text)
        # WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, projects[i]))).click()
        # WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, projects[i+1]))).click()
        # WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, projects[i+2]))).click()
        # WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, projects[i+3]))).click()
        # WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, projects[i+4]))).click()
        projects[i].click()
        # projects[i+1].click()
        # projects[i+2].click()
        # projects[i+3].click()
        # projects[i+4].click()
        
        submit_btn_xpath = '/html/body/div/div[4]/div[4]/form/div/div[1]/p[1]/input'
        submit_btn = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, submit_btn_xpath)))
        submit_btn.click()
        
        try:
            missing_xpath = '/html/body/div/div[4]/div[2]/div/div/div/span/span'
            missing = driver.find_element_by_xpath(missing_xpath)
            if missing:
                driver.refresh()
        except NoSuchElementException:
            pass
        
        try:
            no_result_xpath = '/html/body/div/div[4]/div[2]/div/div/div/span/span'
            no_result = driver.find_element_by_xpath(no_result_xpath)
            if no_result:
                driver.back()
        except NoSuchElementException:
            pass
        
        # project_tbl_class = 'table table-responsive table-striped table-bordered responsiveTable transposeTable'
        # project_tbl = driver.find_element_by_class_name(project_tbl_class)
        
        try:
            project_tbl_data = getTableData()
        except NoSuchElementException:
            continue
        
        ### store data if there is data
        if len(project_tbl_data) > 0:
            project_tbl_df = project_tbl_data[0]
            project_tbl_df.columns = ['Project Name','Street Name','Type','Postal District','Market Segment','Tenure','Type of Sale'
                                         ,'No. of Units','Price','Nett Price','Area (Sqft)','Type of Area','Floor Level','Unit Price ($psf)'
                                         ,'Date of Sale']
            print('%s records found' %project_tbl_df.shape[0])
            df = df.append(project_tbl_df, ignore_index=True)
        
        if i % 20 == 0:
            if not os.path.exists('output'):
                os.makedirs('output')
            df.to_excel(f"./output/Private_resale_prices_{datetime.now().date()}{saved_projects[-1]}.xlsx", index=False)
            
        ### return to main page
        # print('New Search')
        modify_search_xpath = '/html/body/div/div[4]/form/div[2]/div[4]/input'
        modify_search_btn = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, modify_search_xpath)))
        modify_search_btn.click()
        
        
    
    # driver.close()