# kv_prices
Scripts to scrape info from kv.ee and display the results on a chart.

![Resulting chart](https://i.imgur.com/7sEvuZT.png)

## Setup

* install PostgreSQL and Python 3
* install psycopg2 and bokeh via pip
* replace usernames and passwords in the SQL and Python scripts
* run the database script
* make sure the script can write to /var/www/html/kv_prices/ and Apache is working
* use your favourite terminal multiplexer to run both kv_prices.py (data scraper) and chart.py (data renderer)

I have not tested if these instructions are enough so something _will_ blow up. The data is based on the apartments displayed on the kv.ee's Google Maps implementation. Change the URL in kv_prices.py to suit your needs.

