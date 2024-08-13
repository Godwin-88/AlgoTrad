#!/usr/bin/python
# -*- coding: utf-8 -*-

# insert_symbols.py

import pymysql
import datetime
import bs4
import requests

# Database connection details
db_host = 'localhost'
db_user = 'sec_user'
db_pass = '1120'
db_name = 'securities_master'

# Function to obtain and parse symbols
def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P 500 
    constituents using requests and BeautifulSoup.

    Returns a list of tuples to add to MySQL.
    """
    # Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    # Use requests and BeautifulSoup to download the 
    # list of S&P 500 companies and obtain the symbol table
    response = requests.get(
        "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    soup = bs4.BeautifulSoup(response.text, features="html.parser")

    # This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
    symbolslist = soup.select('table')[0].select('tr')[1:]

    # Obtain the symbol information for each 
    # row in the S&P 500 constituent table
    symbols = []
    for symbol in symbolslist:
        tds = symbol.select('td')
        symbols.append(
            (
                tds[0].select('a')[0].text.strip(),  # Ticker
                'stock', 
                tds[1].text.strip(),  # Name
                tds[3].text.strip(),  # Sector
                'USD', now, now
            )
        )
    return symbols

# Main script to connect to the database and insert symbols
try:
    # Establish a database connection
    con = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
    with con.cursor() as cur:
        # Obtain and parse the S&P 500 symbols
        symbols = obtain_parse_wiki_snp500()

        # Insert the symbols into the 'symbol' table
        for symbol in symbols:
            print(symbol)  # Debugging: check the content of the symbol tuple
            cur.execute(
                "INSERT INTO symbol (ticker, instrument, name, sector, currency, created_date, last_updated_date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                symbol
            )

        # Commit the transaction to save changes to the database
        con.commit()
        print("Symbols successfully added to the database.")
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    # Ensure the connection is closed even if an error occurs
    if con:
        con.close()