# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 12:18:12 2020

@author: joachim nuyttens
"""

from urllib import request
from bs4 import BeautifulSoup
from os.path import exists
import sqlalchemy
import utility as ut
import pandas as pd


def get_letter(url):
    """
    Retrieve html code from url

    Parameters
    ----------
    url : String
        URL

    Returns
    -------
    String
        text in html format

    """
    try:
        letter = request.urlopen(url).read().decode('utf8')
    except:
        ut.error(f"Cannot retrieve web address {url}.")
        return 0
    else:
        return letter

def letter_to_text(letter):
    """
    Transform html to raw text

    Parameters
    ----------
    letter : String
        html to transform

    Returns
    -------
    String
        raw text

    """
    return BeautifulSoup(letter, 'html.parser').get_text()

def strip_letter(letter, start, end):
    """
    Trim text from start to end

    Parameters
    ----------
    letter : String
        text to trim
    start : String
        to match for start trimming window
    end : String
        to match for end of trimming window

    Returns
    -------
    String
        trimmed text

    """
    return letter[letter.find(start):letter.rfind(end)]

def save_letter(letter, filename, folder):
    """
    Write letter to txt file

    Parameters
    ----------
    letter : String
        trimmed text ready for writing to file
    filename : String
        filename without ".txt"
    folder : String
        name of existing folder

    Returns
    -------
    int
        1 in case of success, 0 in case of failure

    """
    file = f'{folder}/{filename}.txt'
    if exists(file):
        ut.error(f"Target file {filename} already exists.")
        return 0
    try:
        f = open(file, 'w')
    except:
        ut.error(f"Cannot create or open {filename}.")
    else:
        f.write(letter)
        f.close()
        ut.progress(f"Successfully written letter to {filename}.")
    return 1

def process_letter(url, filename, folder):
    """
    Driver function to retrieve, process and write letter to file

    Parameters
    ----------
    url : String
        URL
    filename : String
        filename without ".txt"
    folder : String
        name of existing folder

    Returns
    -------
    int
        1 in case of success, 0 in case of failure

    """
    letter = get_letter(url)
    if letter:
        text = strip_letter(
            letter_to_text(letter), 'Recipient', 'Content current as of'
            )
        save_letter(text, filename, folder)
        return 1
    else:
        ut.error(f"Processing of letter {filename} failed.")
        return 0

def get_letter_list(db_connection):
    """
    Load data of letters from database to dataframe.

    Parameters
    ----------
    db_connection 

    Returns
    -------
    Dataframe with all letters loaded from database

    """
    try:
        connection = db_connection.connect()
        df = pd.read_sql("SELECT * FROM list;", connection)
    except Exception as e:
        ut.error("Failed to retrieve dataframe from database.")
        ut.progress(f"Detailed error:\n{e}")
        return 0
    else:
        ut.progress("Data retrieved from database.")
        return df