# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:24:22 2020

@author: guanhua
"""

'''
Restful endpoints query to request
https://services2.hdb.gov.sg/webapp/BP13AWFlatAvail/BP13EBSFlatSearch?
Town=Ang+Mo+Kio&
Flat_Type=SBF&
selectedTown=Ang+Mo+Kio&
Flat=2-Room+Flexi+%28Short+Lease%29&
ethnic=Y&
ViewOption=A&
Block=307C&
DesType=A&
EthnicA=Y&
EthnicM=&
EthnicC=&
EthnicO=&
numSPR=&
dteBallot=201911&
Neighbourhood=N3&
Contract=RC10&
projName=&
BonusFlats1=N&
searchDetails=&
brochure=true

https://services2.hdb.gov.sg/webapp/BP13AWFlatAvail/BP13EBSFlatSearch?
Town=Clementi&
Flat_Type=OBF&
selectedTown=Clementi&
Flat=5-Room%2F3Gen&
ethnic=C&
Block=0&
DesType=A&
EthnicA=&
EthnicM=&
EthnicC=C&
EthnicO=&
numSPR=&
dteBallot=202003&
Neighbourhood=&
Contract=&
projName=&
BonusFlats1=N&
searchDetails=Y&
brochure=true

https://services2.hdb.gov.sg/webapp/BP13AWFlatAvail/BP13EBSFlatSearch?
Town=Ang+Mo+Kio&
Flat_Type=SBF&
selectedTown=Ang+Mo+Kio&
Flat=4-Room&
ethnic=Y&
ViewOption=A&
Block=0&
DesType=A&
EthnicA=Y&
EthnicM=&
EthnicC=&
EthnicO=&
numSPR=&
dteBallot=202011&
Neighbourhood=&
Contract=&
projName=&
BonusFlats1=N&
searchDetails=Y&
brochure=true

'''

import re, os, time, random
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
from urllib.parse import unquote_plus
import argparse


driver = webdriver.Chrome("C:/Users/guanhua/Documents/chromedriver/chromedriver.exe")

def getEthnicQuota(ethnic_string):
    ethnic_dict = {}
    ethnic = ethnic_string.split(', ')
    ethnic = [x.split('-') for x in ethnic]
    for eth in ethnic:
        if eth[0] == 'Malay':
            ethnic_dict['Malay'] = int(eth[1])
        elif eth[0] == 'Chinese':
            ethnic_dict['Chinese'] = int(eth[1])
        elif eth[0] == 'Indian/ Other Races':
            ethnic_dict['Indian/ Other Races'] = int(eth[1])
    return ethnic_dict['Malay'], ethnic_dict['Chinese'], ethnic_dict['Indian/ Other Races']
    
def getUnitAndPrice():
    unit_details_table_xpath = '//*[@id="blockDetails"]/div[7]/table/tbody'
    unit_details_table_rows = driver.find_elements_by_xpath(unit_details_table_xpath)
    for row in range(1, len(unit_details_table_rows)+1):
        columns = driver.find_elements_by_xpath(f'//*[@id="blockDetails"]/div[7]/table/tbody/tr[{str(row)}]/td[*]')
        for col in range(1, len(columns)+1):
            unit_xpath = f'//*[@id="blockDetails"]/div[7]/table/tbody/tr[{str(row)}]/td[{str(col)}]'
            unit = driver.find_element_by_xpath(unit_xpath)
            unit_text = unit.text
            font_color_text = unit.get_attribute("font color")
            hover_details = driver.find_element_by_xpath(f'//*[@id="{unit_text}k"]').text
            # print(hover_details)
            price = 0
            sqm = re.findall('\d+ [sqm]', hover_details)
            
            if font_color_text == '#cc0000':
                IsBooked = True
            else:
                IsBooked = False
            return unit_text, price, sqm, IsBooked

def getBlockData(df, exercise, town, room_type):
    blockData_xpath = '//*[@id="blockDetails"]/div[2]'
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, blockData_xpath)))
    
    block = driver.find_element_by_xpath('//*[@id="blockDetails"]/div[2]/div[2]').text
    street = driver.find_element_by_xpath('//*[@id="blockDetails"]/div[2]/div[4]').text
    pcd = driver.find_element_by_xpath('//*[@id="blockDetails"]/div[3]/div[2]').text
    dpd = driver.find_element_by_xpath('//*[@id="blockDetails"]/div[4]/div[2]').text
    lcd = driver.find_element_by_xpath('//*[@id="blockDetails"]/div[5]/div[2]').text
    ethnic = driver.find_element_by_xpath('//*[@id="blockDetails"]/div[6]/div[2]').text
    
    malay, chinese, indian_others = getEthnicQuota(ethnic)
    
    # unit_text, price, sqm, IsBooked = getUnitAndPrice()

    unit_details_table_xpath = '//*[@id="blockDetails"]/div[7]/table/tbody/tr'
    unit_details_table_rows = driver.find_elements_by_xpath(unit_details_table_xpath)
    
    nrows = len(unit_details_table_rows)
    row = 1
    while nrows != 0:
        # print(f"this is row: {row}")
        
        unit_details_table_columns = driver.find_elements_by_xpath(f'//*[@id="blockDetails"]/div[7]/table/tbody/tr[{row}]/td')
        # print(f'there are {len(unit_details_table_columns)} columns')
        
        for col in range(1, len(unit_details_table_columns)+1):
            # print(f"this is row: {row}, column: {col}")
            unit_xpath = f'//*[@id="blockDetails"]/div[7]/table/tbody/tr[{row}]/td[{col}]'
            unit = driver.find_element_by_xpath(unit_xpath)
            unit_text = unit.text
            font_color_text = unit.get_attribute("color")
            
            if unit_text == '3Gen':
                room_type = '3Gen' # set room_type 
                continue # force for loop to go to next row
            elif unit_text == '5-Room': 
                room_type = '5-Room' # set room_type 
                continue # force for loop to go to next row
                        
            try:
                hover_details = driver.find_element_by_id(f"{unit_text}k")
                if hover_details:
                    hover_details_text = hover_details.get_attribute('title')
                    # print(hover_details_text)
                    price = hover_details_text.split('<br>____________________<br>')[0]
                    sqm = hover_details_text.split('<br>____________________<br>')[1].split()[0]
                    if font_color_text == '#cc0000':
                        IsBooked = True
                    else:
                        IsBooked = False
            except:
                price = None
                sqm = None
                IsBooked = True

            print(block, street, pcd, dpd, lcd, malay, chinese, indian_others, unit_text, price, sqm,IsBooked)
            df = df.append({'HDB Exercise':exercise, 'Town':town,'Room Type':room_type,'Block':block,'Street':street,'Probable Completion Date':pcd,\
                            'Delivery Possession Date':dpd,'Lease Commencement Date':lcd,\
                            'Ethic Quota-Malay':malay,'Ethic Quota-Chinese':chinese,'Ethic Quota-Indian Others':indian_others,'Unit':unit_text,\
                            'Price':price,'Sqm':sqm,'IsBooked':IsBooked}, ignore_index=True)
            
        row += 1
        nrows -= 1
        # print(nrows)
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('exercise', help="default: 'all' or choose either 'SBF' or 'OBF'")
    parser.add_argument('town', help="default: 'all' or choose from 'Ang Mo Kio','Bukit Batok','Bedok','Bishan','Bukit Merah','Bukit Panjang','Bukit Timah',\
                        'Central','Choa Chu Kang',\
                        'Clementi','Geylang','Hougang','Jurong East','Jurong West','Kallang/Whampoa','Marine Parade','Punggol',\
                        'Pasir Ris','Queenstown','Sembawang','Serangoon','Sengkang','Tampines','Toa Payoh','Woodlands','Yishun' use | operator to separate multiple eg. 'Tampines|Clementi' ")
    parser.add_argument('flat', help="default: 'all' or choose from '2-Room', '3-Room', '4-Room', '5-Room', '3Gen', 'Executive' use | operator to separate multiple eg. '4-Room|5-Room' ")
    args = parser.parse_args()
    
    if args.town != 'all':
        towns = args.town.split('|')
    else:
        towns=['Ang Mo Kio','Bukit Batok','Bedok','Bishan','Bukit Merah','Bukit Panjang','Bukit Timah','Central','Choa Chu Kang',\
                'Clementi','Geylang','Hougang','Jurong East','Jurong West','Kallang/Whampoa','Marine Parade','Punggol',\
                'Pasir Ris','Queenstown','Sembawang','Serangoon','Sengkang','Tampines','Toa Payoh','Woodlands','Yishun']
    towns=[re.sub(' ','+',town) for town in towns]
    
    
    if args.flat != 'all':
        flats = []
        argflats = args.flat.split('|')
        if '2-Room' in argflats:
            flats += ['2-Room+Flexi+%28Short+Lease%29', '2-Room+Flexi+%28Short+Lease%2F99-Year+Lease%29']
        if '3-Room' in argflats:
            flats += ['3-ROOM']
        if '4-Room' in argflats:
            flats += ['4-Room']
        if '5-Room' in argflats:
            flats += ['5-Room','5-Room%2F3Gen']
        if '3Gen' in argflats:
            flats += ['5-Room%2F3Gen']
    else:
        flats = ['2-Room+Flexi+%28Short+Lease%29', '2-Room+Flexi+%28Short+Lease%2F99-Year+Lease%29', '3-ROOM','4-Room', '5-Room', '5-Room%2F3Gen', 'Executive']
    
    #TODO
    '3-Room+%28income+ceiling+%247%2C000%29'
    '3-Room+%28income+ceiling+%2414%2C000%29'
    
    if args.exercise != 'all':
        hdb_exercises = args.exercise.split('|')
    else:
        hdb_exercises = ['SBF','OBF']


    flatsearchhttp = 'https://services2.hdb.gov.sg/webapp/BP13AWFlatAvail/BP13EBSFlatSearch?'
    print(towns,flats,hdb_exercises)
    df = pd.DataFrame(columns = ['HDB Exercise', 'Town', 'Room Type', 'Block', 'Street', 'Probable Completion Date', 'Delivery Possession Date', 'Lease Commencement Date', \
                                 'Ethic Quota-Malay', 'Ethic Quota-Chinese', 'Ethic Quota-Indian Others', 'Unit', 'Price', 'Sqm', 'IsBooked'])
    
    ## Static Params
    DesType = 'A' #'S'=Standard 'A'=Any, 'P'=Premium
    ethnic = 'Y'
    ViewOption = 'A'
    projName = 'A'
    brochure = 'true'
    Block = '0'
    EthnicA='Y'
    EthnicM=''
    EthnicC=''
    EthnicO=''
    numSPR=''
    Neighbourhood=''
    Contract=''
    BonusFlats1='N'
    searchDetails='Y'
    
    for exercise in hdb_exercises:
        for mytown in towns:
            print(mytown)
            for myflat in flats:
                print(myflat)
                
                ## Dynamic Params
                town=mytown #'Ang+Mo+Kio'
                flat_type = exercise # 'SBF' # 'OBF'
                dteBallot = '202011' if exercise == 'SBF' else '202003' # 'OBF'
                flat = myflat #'2-Room%20Flexi%20(Short%20Lease)'
                
                params = ['Town='+town, 'Flat_Type='+flat_type, 'selectedTown='+town, 'Flat='+flat, 'ethnic='+ethnic, 'ViewOption='+ViewOption,\
                          'Block='+Block, 'DesType='+DesType, 'EthnicA='+EthnicA, 'EthnicM='+EthnicM, 'EthnicC='+EthnicC, 'EthnicO='+EthnicO,\
                          'numSPR='+numSPR, 'dteBallot='+dteBallot, 'Neighbourhood='+Neighbourhood, 'Contract='+Contract, 'projName='+projName,\
                          'BonusFlats1='+BonusFlats1, 'searchDetails='+searchDetails, 'brochure='+brochure]
                query = '&'.join(params)
                # print(flatsearchhttp+query)
                driver.get(flatsearchhttp+query)
                
                block_details_xpath = '//*[@id="blockDetails"]'
                block_details = driver.find_element_by_xpath(block_details_xpath)
                if block_details:
                    print('Block Details Present')
                    block_details_table_xpath = '//*[@id="blockDetails"]/div[1]/table/tbody/tr[*]'
                    block_details_table_rows = driver.find_elements_by_xpath(block_details_table_xpath)
                    # print(len(block_details_table_rows))
                    for row in range(1, len(block_details_table_rows)+1):
                        # print(row)
                        columns = driver.find_elements_by_xpath(f'//*[@id="blockDetails"]/div[1]/table/tbody/tr[{str(row)}]/td[*]')
                        # print(len(columns))
                        for col in range(1, len(columns)+1):
                            # print(col)
                            cell_xpath = f'//*[@id="blockDetails"]/div[1]/table/tbody/tr[{str(row)}]/td[{str(col)}]/div'
                            cell = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, cell_xpath)))
                            if cell:
                                blue_cell_xpath = f'//*[@id="blockDetails"]/div[1]/table/tbody/tr[{str(row)}]/td[{str(col)}]/div/font/a/font'
                                blue_cell = driver.find_elements_by_xpath(blue_cell_xpath)
                                if blue_cell:
                                    cell = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, cell_xpath)))
                                    driver.execute_script('arguments[0].click();', cell)
                                    print('Clicked')
                                    df = getBlockData(df, exercise, unquote_plus(mytown),unquote_plus(myflat))
                                    
                                    if df.shape[0] % 100 == 0:
                                        if not os.path.exists('output'):
                                            os.makedirs('./output')
                                        df.to_csv(f'./output/sbf_obf_non_booked_{datetime.now().date()}.csv', index=False)
                            
                            wait_secs = random.randint(6,13)
                            print(f"wait for {wait_secs} seconds..")
                            time.sleep(wait_secs) #wait
    
    print(df.shape)
    if not os.path.exists('output'):
        os.makedirs('./output')
    df.to_csv(f'./output/sbf_obf_non_booked_{datetime.now().date()}.csv', index=False)