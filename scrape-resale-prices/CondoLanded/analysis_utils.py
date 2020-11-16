# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 12:09:54 2020

@author: guanhua
"""

import matplotlib.pyplot as plt
import numpy as np

def showAvgResalePrice(mycondo, date_idx):
    mycondo_prices = mycondo.groupby('Date of Sale (mon-year)').agg({'Price':'mean'})
    mycondo_prices = mycondo_prices.reindex(date_idx, fill_value=0)

    ax = mycondo_prices.plot(kind='bar', stacked=True, figsize=(16,8), title='Average Resale Prices')
    ax.legend(bbox_to_anchor=(1, 1))
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height+1),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points')
    
    mycondoname = mycondo['Project Name'].unique().tolist()[0]
    
    ax.set_ylabel('$ Price')
    plt.suptitle(mycondoname)
    plt.show()
    
    
def showAvgPsf(mycondo, date_idx):
    mycondo_prices = mycondo.groupby('Date of Sale (mon-year)').agg({'Psf':'mean'})
    mycondo_prices = mycondo_prices.reindex(date_idx, fill_value=0)

    ax = mycondo_prices.plot(kind='bar', stacked=False, figsize=(16,8), title='Average Resale Prices $PSF')
    ax.legend(bbox_to_anchor=(1, 1))
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0 and height < np.inf:
            ax.annotate(int(round(height)),\
                        (x+width/2, y+height+1),\
                        ha='center', va='center', xytext=(0, 3), textcoords='offset points')
    
    mycondoname = mycondo['Project Name'].unique().tolist()[0]
    
    ax.set_ylabel('$ Psf')
    plt.suptitle(mycondoname)
    plt.show()