# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 16:29:53 2022

@author: leebond
"""
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
from datetime import datetime

def show_past_n_months_resale_volume(hdb, n_months):
    hdb_vol = hdb[hdb['Flat Type'].isin(['2-Room','3-Room','4-Room','5-Room','Executive'])].\
    groupby(['Resale Registration Date','Flat Type']).agg({'Town':'count'}).unstack('Flat Type').fillna(0).reset_index()
    hdb_vol.columns = ['Resale Registration Date','2-Room','3-Room','4-Room','5-Room','Executive']
    hdb_vol['Resale Registration Date'] =  pd.to_datetime(hdb_vol['Resale Registration Date'], format='%b %Y')
    hdb_vol = hdb_vol.sort_values(by=['Resale Registration Date'], ascending=True)
    hdb_vol['Resale Registration Date'] = hdb_vol['Resale Registration Date'].apply(lambda x: datetime.strftime(x, '%b %Y'))
    hdb_vol.set_index(['Resale Registration Date'], inplace=True)
    ax = hdb_vol.plot(kind='bar', stacked=True, figsize=(12,8), title=f'Resale Volume Over Past {n_months} Months as of {datetime.now().date()}')
    ax.legend(bbox_to_anchor=(1, 1))
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height/2),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points')
    ax.set_ylabel('Resale Volume')
    plt.show()
    
    
def show_resale_volume_by_town(hdb, n_months):
    hdb_vol = hdb[hdb['Flat Type'].isin(['2-Room','3-Room','4-Room','5-Room','Executive'])].\
    groupby(['Town','Flat Type']).agg({'Town':'count'}).unstack('Flat Type').fillna(0).reset_index()
    
    hdb_vol.columns = ['Town Name','2-Room','3-Room','4-Room','5-Room','Executive']
    hdb_vol
    
    ax = hdb_vol.plot(kind='bar', stacked=True, figsize=(12,8), x='Town Name',\
                      title=f'Total Resale Volume Over Past {n_months} Months by Town as of {datetime.now().date()}')
    ax.legend(bbox_to_anchor=(1, 1))
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height/2),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points')
    ax.set_ylabel('Resale Volume')
    plt.show()
    
def show_price_distribution(hdb):
    fig, ax = plt.subplots(figsize=(10,6))
    hdb['Price per Sqft'].plot.hist(bins=25, alpha=0.5, title=f'Resale Price $ Psf Distribution as of {datetime.now().date()}', ax=ax)
    five_stats = [round(hdb['Price per Sqft'].min(),1), round(hdb['Price per Sqft'].max(),1),\
    round(hdb['Price per Sqft'].mean(),1), round(hdb['Price per Sqft'].std(),1), round(hdb['Price per Sqft'].median(),1),\
          round(hdb['Price per Sqft'].kurtosis(),1), round(hdb['Price per Sqft'].skew(),1)       ]
    ax.set_xlabel('Price $ Psf')
    ax.set_ylabel('Number of Resale Transactions')
    legend = list(zip(['min', 'max','mean','stddev','median', 'skew', 'kurtosis'] ,five_stats))
    print(legend)
    # ax.text(0.99,0.99,legend, ha='center', va='center',transform=ax.transAxes)
    
    plt.show()
    
def show_price_cumulative_distribution(hdb):
    fig, ax = plt.subplots(figsize=(10,6))
    hdb['Price per Sqft'].plot.hist(bins=25, alpha=0.5, ax=ax, title=f'Resale Price $ Psf Distribution as of {datetime.now().date()}', cumulative = True)
    ax.set_yticklabels(np.arange(0,(hdb.shape[0]+1)/hdb.shape[0]*100, round(1/8*100)))
    ax.set_ylim(0,hdb.shape[0])
    
def show_median_prices_by_room_type_and_month(hdb):
    hdb_median_prices_bytime = hdb.groupby(['Flat Type','Resale Registration Date']).agg({'Price per Sqft':'median'}).reset_index()
    hdb_median_prices_bytime['Resale Registration Date'] =  pd.to_datetime(hdb_median_prices_bytime['Resale Registration Date'], format='%b %Y')
    hdb_median_prices_bytime = hdb_median_prices_bytime.sort_values(by=['Flat Type','Resale Registration Date'], ascending=True)
    hdb_median_prices_bytime['Resale Registration Date'] = hdb_median_prices_bytime['Resale Registration Date'].apply(lambda x: datetime.strftime(x, '%b %Y'))
    hdb_median_prices_bytime.set_index(['Flat Type','Resale Registration Date'], inplace=True)
    
    hdb_vol_bytime = hdb.groupby(['Flat Type','Resale Registration Date']).agg({'Town':'count'}).reset_index()
    hdb_vol_bytime.columns = ['Flat Type','Resale Registration Date','Resale Volume']
    hdb_vol_bytime['Resale Registration Date'] =  pd.to_datetime(hdb_vol_bytime['Resale Registration Date'], format='%b %Y')
    hdb_vol_bytime = hdb_vol_bytime.sort_values(by=['Flat Type','Resale Registration Date'], ascending=True)
    hdb_vol_bytime['Resale Registration Date'] = hdb_vol_bytime['Resale Registration Date'].apply(lambda x: datetime.strftime(x, '%b %Y'))
    hdb_vol_bytime.set_index(['Flat Type','Resale Registration Date'], inplace=True)
    
    fig, ax = plt.subplots(figsize=(20,8))
    hdb_median_prices_bytime.plot(kind='line', color = '#0080FF', ax=ax)
    ax = hdb_vol_bytime.plot(kind='bar', figsize=(20,8), color = '#00b834', ax = ax)
    
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width, y+height),\
                        ha='center', va='center', xytext=(-3, 10), textcoords='offset points')
    ax.set_title('Resale Median Price $ Psf and Volume by Room Type and Resale Month as of {datetime.now().date()}')
    ax.set_ylabel('Price $ Psf and Resale Volume')
    plt.show()
    
def show_median_prices_by_town_and_room_type(hdb):
    hdb_median_prices = hdb.groupby(['Town','Flat Type']).agg({'Price per Sqft':'median'})
    fig, ax = plt.subplots(figsize=(12,28))
    hdb_median_prices.plot(kind = 'barh', color='#0080FF', ax=ax)
    # plt.suptitle(f"Median Price psf by Town", fontsize=18)
    ax.set_xlabel("Price $ Psf", fontsize=12)
    ax.set_title(f'Resale Median Price $ Psf by Town and Room Type as of {datetime.now().date()}')
    ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if width > 0 and width < np.inf:
            ax.annotate(int(round(width)),\
                        (x+width+20, y),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points')
    
    ax.legend(['Price $ Psf'])
    plt.show()
    
def show_median_prices_by_town_and_room_type_per_remaining_lease_year(hdb):
    hdb_median_prices_remaining_lease = hdb.groupby(['Town','Flat Type']).agg({'Price per Sqft per Remaining Lease year':'median'})
    fig, ax = plt.subplots(figsize=(12,28))
    hdb_median_prices_remaining_lease.plot(kind = 'barh', color='#0080FF', ax=ax)
    # plt.suptitle(f"Median Price psf by Town", fontsize=18)
    ax.set_xlabel("Price $ Psf", fontsize=12)
    ax.set_title(f'Resale Median Price $ Psf by Town Name and Room Type as of {datetime.now().date()}')
    ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    ax.legend(['Price $ Psf'])
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if width > 0 and width < np.inf:
            ax.annotate(round(width,2),\
                        (x+width, y),\
                        ha='center', va='center', xytext=(20, 3), textcoords='offset points')
    
    plt.show()
    
def show_remaining_lease_year_by_town(hdb, n_months):
    remaining_lease = hdb.groupby('Town').agg({'Remaining Lease in Months':'mean'}).reset_index()
    remaining_lease['Remaining Lease in Years'] = remaining_lease['Remaining Lease in Months']//12
    remaining_lease['Remaining Lease in (Months)'] = round(remaining_lease['Remaining Lease in Months']%12)
    remaining_lease['Remaining Lease'] = remaining_lease['Remaining Lease in Years'].\
    astype(int).astype(str) + ' years ' + remaining_lease['Remaining Lease in (Months)'].astype(int).astype(str) + ' months'
    remaining_lease = remaining_lease.sort_values(by = 'Remaining Lease in Months')
    
    fig, ax = plt.subplots(figsize=(14,10))
    remaining_lease.plot(kind = 'barh', color='#0080FF', x='Town', y='Remaining Lease in Months', ax=ax)
    ax.set_xticklabels(np.round(np.arange(0,101,100/6)))
    ax.legend(['Average Remaining Lease'])
    ax.set_xlabel('Remaining Lease (Years)')
    ax.set_xlim(0,1300)
    cnt = 0
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if width > 0 and width < np.inf:
            ax.annotate(remaining_lease['Remaining Lease'].iloc[cnt],\
                        (x+width+100, y+height-0.7),\
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')
        cnt+=1
    
    ax.set_title(f'Average Remaining Lease of Transacted HDB Resale Units by Town Over Past {n_months} Months as of {datetime.now().date()}')
    
    plt.show()
    
    
def show_remaining_lease_year_by_town_for_hdb_older_than_n_age(hdb, n):
    hdb_median_prices = hdb[hdb['Remaining Lease (Year)']<n].groupby(['Town','Flat Type']).agg({'Price per Sqft':'median'}).\
    sort_values(by='Price per Sqft')
    fig, ax = plt.subplots(figsize=(12,28))
    hdb_median_prices.plot(kind = 'barh', color='#0080FF', ax=ax)
    # plt.suptitle(f"Median Price psf by Town", fontsize=18)
    ax.set_xlabel("Price $ Psf", fontsize=12)
    ax.set_title(f'Price $ Psf by Town and Room Type of HDBs < {n} Years of Lease as of {datetime.now().date()}')
    ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if width > 0 and width < np.inf:
            ax.annotate(int(round(width)),\
                        (x+width+20, y),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points')
    
    ax.legend(['Price $ Psf'])
    plt.show()
    
    
def show_past_n_months_mean_psf_of_town(hdb, n_months, mytown):
    twn = hdb[hdb['Town'] == mytown]
    twn_px = twn[twn['Flat Type'].isin(['3-Room','4-Room','5-Room','Executive'])].\
    groupby(['Resale Registration Date','Flat Type']).agg({'Price per Sqft':'mean'}).unstack('Flat Type').fillna(0).reset_index()
    twn_px.columns = ['Resale Registration Date','3-Room','4-Room','5-Room','Executive']
    twn_px['Resale Registration Date'] =  pd.to_datetime(twn_px['Resale Registration Date'], format='%b %Y')
    twn_px = twn_px.sort_values(by=['Resale Registration Date'], ascending=True)
    twn_px['Resale Registration Date'] = twn_px['Resale Registration Date'].apply(lambda x: datetime.strftime(x, '%b %Y'))
    twn_px.set_index(['Resale Registration Date'], inplace=True)
    
    fig, ax = plt.subplots(figsize=(12,8))
    twn_px.plot(kind='bar', stacked=False, title=f'Resale Price Over Past {n_months} Months as of {datetime.now().date()}', ax=ax)
    ax.legend(bbox_to_anchor=(1, 1))
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height+10),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points', rotation = 90)
    plt.suptitle(f"{mytown}", fontsize=18)
    ax.set_ylabel('Resale Volume')
    plt.show()
    
def show_past_n_months_mean_psf_by_floor_and_flat_type(hdb, n_months, mytown):
    twn = hdb[hdb['Town'] == mytown]
    toplot = twn.groupby(['Town','Storey','Flat Type']).\
    agg({'Town':'count', 'Price':['mean','median'], 'Price per Sqm':['mean','median'],\
                                                           'Price per Sqft':['mean','median']}).reset_index()
    toplot.columns = ['Town','Storey','Flat Type','Total Units','Average Price','Median Price',\
                      'Average Price per Sqm','Median Price per Sqm',\
                      'Average Price per Sqft','Median Price per Sqft']
    toplot = toplot.round({'Average Price':2,'Median Price':2,\
                      'Average Price per Sqm':2,'Median Price per Sqm':2,\
                      'Average Price per Sqft':2,'Median Price per Sqft':2})
    toplot['Storey Range + Room Type'] = toplot['Storey'] + ' ' + toplot['Flat Type']
    
    
    fig, ax = plt.subplots(figsize=(20,8))
    
    toplot.plot(kind='bar', x = 'Storey Range + Room Type',\
                     y=['Average Price per Sqft','Median Price per Sqft'], ax=ax)
    
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height+10),\
                        ha='center', va='center', xytext=(0, 9), textcoords='offset points', rotation = 90)
    
    plt.suptitle(f"{mytown}", fontsize=18)
    ax.set_ylabel("Price $ Psf", fontsize=12)
    ax.set_title(f'Historical Average and Median Prices per Sqft over the past {n_months} months as of {datetime.now().date()}')
    plt.show()
    
    
def show_past_n_months_mean_psf_by_floor_and_flat_type_and_street(hdb, n_months, mystreet):
    town_street = hdb[hdb['Street'].isin([mystreet])]
    toplot = town_street.groupby(['Town','Storey','Flat Type']).\
    agg({'Town':'count', 'Price':['mean','median'], 'Price per Sqm':['mean','median'],\
                                                           'Price per Sqft':['mean','median']}).reset_index()
    toplot.columns = ['Town','Storey','Flat Type','Total Units','Average Price','Median Price',\
                      'Average Price per Sqm','Median Price per Sqm',\
                      'Average Price per Sqft','Median Price per Sqft']
    toplot = toplot.round({'Average Price':2,'Median Price':2,\
                      'Average Price per Sqm':2,'Median Price per Sqm':2,\
                      'Average Price per Sqft':2,'Median Price per Sqft':2})
    toplot['Storey Range + Room Type'] = toplot['Storey'] + ' ' + toplot['Flat Type']
    
    fig, ax = plt.subplots(figsize=(20,8))
    
    toplot.plot(kind='bar', x = 'Storey Range + Room Type', y=['Average Price per Sqft','Median Price per Sqft'], ax=ax)
    
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height+10),\
                        ha='center', va='center', xytext=(0, 9), textcoords='offset points', rotation = 90)
    
    plt.suptitle(f"{mystreet}", fontsize=18)
    ax.set_ylabel("Price $ Psf", fontsize=12)
    ax.set_title(f'Historical Average and Median Prices per Sqft over the past {n_months} months as of {datetime.now().date()}')
    plt.show()
    
def show_past_n_months_psf_of_flat_model(hdb, n_months, flat_model):
    dbss = hdb[hdb['Flat Model']==flat_model]

    toplot = dbss.groupby(['Town','Flat Type']).\
    agg({'Town':'count', 'Price':['mean','median'], 'Price per Sqm':['mean','median'],\
                                                           'Price per Sqft':['mean','median']}).reset_index()
    toplot.columns = ['Town','Flat Type','Total Units','Average Price','Median Price',\
                      'Average Price per Sqm','Median Price per Sqm',\
                      'Average Price per Sqft','Median Price per Sqft']
    toplot = toplot.round({'Average Price':2,'Median Price':2,\
                      'Average Price per Sqm':2,'Median Price per Sqm':2,\
                      'Average Price per Sqft':2,'Median Price per Sqft':2})
    toplot['Town + Room Type'] = toplot['Town'] + ' ' + toplot['Flat Type']
    
    fig, ax = plt.subplots(figsize=(20,8))
    
    ax = toplot.plot(kind='bar', x = 'Town + Room Type', y=['Average Price per Sqft','Median Price per Sqft'], ax=ax)
    
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height+10),\
                        ha='center', va='center', xytext=(0, 9), textcoords='offset points', rotation = 90)
    
    plt.suptitle(f"DBSS", fontsize=18)
    ax.set_ylabel("Price $ Psf", fontsize=12)
    ax.set_title(f'Historical Average and Median Prices per Sqft over the past {n_months} months as of {datetime.now().date()}')
    plt.show()