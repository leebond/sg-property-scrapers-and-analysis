# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:37:25 2020

@author: guanhua
"""
import re
import pandas as pd
from datetime import datetime

def getRemainingLeaseYear(row):
    r = row.split('\n')[0]
    r = re.search('\d+', r).group()
    return int(r)

def getRemainingLeaseMonth(row):
    r = row.split('\n')
    if len(r) > 1:
        r = r[1]
        r = re.search('\d+', r).group()
        return int(r)
    else:
        return int(0)
    
def getFloorArea(row):
    return float(row.split('\n')[0])

def getModelType(row):
    try:
        r = row.split('\n')[1]
        return r
    except:
        return None
    
def cleanPrice(row):
    r = re.sub('[^0-9]','',row)
    return float(r.strip('$'))/100

def getTownName(row):
    r = row.split()[1:]
    return ' '.join(r)
    

def preprocessHDBdf(hdb):
    hdb['Street'] = hdb['Street'].str.strip()

    flat_type_conversion = {1:'1-Room',2:'2-Room',3:'3-Room',4:'4-Room',5:'5-Room',6:'Executive',8:'Multi-Generation'}
    hdb.replace({'Room Type': flat_type_conversion}, inplace=True)
    
    hdb['Remaining Lease (Year)'] = hdb['Remaining Lease'].apply(getRemainingLeaseYear)
    hdb['Remaining Lease (Month)'] = hdb['Remaining Lease'].apply(getRemainingLeaseMonth)
    hdb['Remaining Lease in Months'] = hdb['Remaining Lease (Year)']*12 + hdb['Remaining Lease (Month)']
    
    hdb['Floor Area Sqm'] = hdb['Sqm'].apply(getFloorArea)
    hdb['Model Type'] = hdb['Sqm'].apply(getModelType)
    
    hdb['Price'] = hdb['Price'].apply(cleanPrice)
    hdb['Price'] = hdb['Price'].astype(float)
    hdb['Town Name'] = hdb['Town'].apply(getTownName)
    
    SQM_to_SQFT = 10.764
    hdb['Floor Area Sqft'] = hdb['Floor Area Sqm']*SQM_to_SQFT
    hdb['Price per Sqm'] = hdb['Price']/hdb['Floor Area Sqm']
    hdb['Price per Sqft'] = hdb['Price']/hdb['Floor Area Sqft']
    hdb['Price per Sqft per Remaining Lease year'] = hdb['Price per Sqft']/hdb['Remaining Lease in Months']*12
    hdb['Storey Range + Room Type'] = hdb['Storey'] + ' ' + hdb['Room Type']
    
    hdb['Resale Registration Date'] = pd.to_datetime(hdb['Resale Registration Date'], format='%b %Y')
    hdb['Resale Registration Date'] = hdb['Resale Registration Date'].apply(lambda x: datetime.strftime(x, '%b %Y'))
    hdb = hdb.sort_values(by = 'Resale Registration Date')
    
    return hdb
