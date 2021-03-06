
# Description
This folder contains the HDB resale transaction web scraper 
- usage: run `python scrape-HDB-resale-historical-prices.py` in your command line scrapes transaction details of HDB Resale units.
Note: To scrape the full 12 months of HDB resale data may take up to an hour depending on the speed of your internet and machine.

### Analysis
I am in progress of adding a iPython Notebook that analyses HDB resale transactions.
You may find the analysis in `HDB Resale Analysis.ipynb` in time to come.

Here are some prelimnary analyses:

- Resale Volume

<img src=".\public\resale_volume.png" width="640px">

- Resale Volume by Town

<img src=".\public\resale_volume_bytown.png" width="640px">

- Resale Price Distribution

<img src=".\public\price_distribution.png" width="640px">

- Resale Median Prices by Resale Date

<img src=".\public\hdb_median_prices.png" width="960px" height="480px">

- Resale Median Prices psf over the past 12 months by Town Name and Room Type

<img src=".\public\hdb_median_prices_byTown.png" width="640px">

- Average Remaining Lease of Transacted HDB Resale Units by Town

<img src=".\public\remaining_lease_byTown.png" width="640px">

### Advanced Analysis
- refer to .\.ipynb file
