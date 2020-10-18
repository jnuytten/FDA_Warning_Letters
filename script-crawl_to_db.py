# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 13:44:48 2020

@author: joachim nuyttens
"""

import webcrawl as wc
import utility as ut



url = 'https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters'
sql_connection = ut.create_sql_connection('mysql://joachim:python@localhost/warning_letters?unix_socket=/run/mysqld/mysqld.sock&charset=utf8mb4')

data = wc.crawl_site(url, 317)    
wc.save_data(data, sql_connection)