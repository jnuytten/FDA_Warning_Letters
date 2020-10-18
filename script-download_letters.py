#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 21:08:52 2020

@author: joachim nuyttens
"""

import pageproc as pp
import utility as ut
from os.path import exists

sql_connection = ut.create_sql_connection(
    'mysql://joachim:python@localhost/warning_letters?unix_socket=/run/mysqld/mysqld.sock'
    )
df = pp.get_letter_list(sql_connection)

for index, row in df.iterrows():
    file = "letters/" + row['id'] + '.txt'
    if exists(file):
        pass
    else:
        print(f"Writing letter to file: {file}")
        pp.process_letter(row['link'], row['id'], "letters")
