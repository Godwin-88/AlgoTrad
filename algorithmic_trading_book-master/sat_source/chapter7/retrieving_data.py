#!/usr/bin/python
# -*- coding: utf-8 -*-

# retrieving_data.py

import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Database connection details
db_host = 'localhost'
db_user = 'sec_user'
db_pass = '1120'
db_name = 'securities_master'

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")

# SQL query to get Google adjusted close prices
sql = """SELECT dp.price_date, dp.adj_close_price
         FROM symbol AS sym
         INNER JOIN daily_price AS dp
         ON dp.symbol_id = sym.id
         WHERE sym.ticker = 'GOOG'
         ORDER BY dp.price_date ASC;"""

# Create a pandas dataframe from the SQL query
goog = pd.read_sql_query(sql, con=engine, index_col='price_date')

# Output the dataframe tail
print(goog.head())
