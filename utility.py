# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:12:16 2020

@author: joachim nuyttens
"""

from sqlalchemy import create_engine
import datetime

def error(message):
    print("Error: " + message)

def progress(message):
    print("-- " + message)

def create_sql_connection(connect_string):
    return create_engine(connect_string)

def dateformat_us_iso(date):
    """
    Transform date format from US to ISO format, to allow input in DB.

    Parameters
    ----------
    date : String
    in date format mm/dd/yyyy (ex. 08/18/2020)
    Returns
    -------
    String

    """
    return datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
