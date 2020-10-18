# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 17:22:46 2020

@author: joachim nuyttens
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import pandas as pd
import time
import re
import utility as ut
import sqlalchemy

def make_driver(browser = 'Chrome'):
    """
    Create webdriver.

    Parameters
    ----------
    browser : String, optional
        The default is 'Chrome'.

    Returns
    -------
    driver : WebDriver object
    """
    if browser == 'Chrome':
        driver = webdriver.Chrome()
        driver.maximize_window()
    return driver

def crawl_page(driver):
    """
    Crawl a single page with warning letters and retrieve info.
    
    Parameters
    ----------
    driver : WebDriver object

    Returns
    -------
    dictionary, containing the retrieved info
    """
    # initiate lists
    posted, issued, company, office, subject, link = [], [], [], [], [], []
    # count the number of lines in table (exclude header)
    count = len(
        driver.find_elements_by_xpath(
            "//table[@id='DataTables_Table_0']/*/tr/td[1]"
            ))
    # loop over lines
    for i in range (1, count + 1):
        # retrieve text of td tags
        letter_info = driver.find_elements_by_xpath(
            f"//table[@id='DataTables_Table_0']/*/tr[{i}]/td"
            )
        # retrieve href attribute of link
        letter_link = driver.find_elements_by_xpath(
            f"//table[@id='DataTables_Table_0']/*/tr[{i}]/td[3]/a"
            )
        # store retrieve info in lists, dates transformed to ISO format
        posted.append(ut.dateformat_us_iso(letter_info[0].text.strip()))
        issued.append(ut.dateformat_us_iso(letter_info[1].text.strip()))
        company.append(letter_info[2].text.strip())
        office.append(letter_info[3].text.strip())
        subject.append(letter_info[4].text.strip())
        link.append(letter_link[0].get_attribute('href'))
    return {
        'posted': posted,
        'issued': issued,
        'company': company,
        'office': office,
        'subject': subject,
        'link': link
        }


def go_next_page(driver):
    """
    Navigate to next page using "Next" button, return 1 if succesfull

    Parameters
    ----------
    driver : WebDriver object

    Returns
    -------
    int, 1 / 0 if succesfull / not succesfull

    """
    try:
        next_button = driver.find_element_by_link_text('Next')
    except:
        ut.error("Failed to click 'Next' button.")
        return 0
    else:
        next_button.click()
        return 1

def crawl_site(url, page_count_max, skip_page = 0):
    """
    Crawl website by navigating through different pages.

    Parameters
    ----------
    url : String
        first webpage
    page_count_max : int
        maximum number of pages to crawl

    Returns
    -------
    site_df: Dataframe

    """
    driver = make_driver()
    driver.get(url)
    # wait 2 seconds for page to load
    time.sleep(2)
    page_count = 1
    # if we need to skip pages
    while skip_page > 0:
        go_next_page(driver)
        skip_page -= 1
        time.sleep(2)
    # crawl first page and store data in new site dataframe
    page_data = crawl_page(driver)
    df_columns = ['posted', 'issued', 'company', 'office', 'subject', 'link']
    site_df = pd.DataFrame(
        page_data,
        columns = df_columns,
        index = [get_unique_id(link) for link in page_data['link']]
        )
    ut.progress("First page crawled and saved in dataframe.")
    # navigate to second and subsequent pages up to page_count_max
    while go_next_page(driver) and page_count < page_count_max:
        page_count += 1
        # wait 2 seconds to not overload server
        time.sleep(2)
        # crawl page and append data to site dataframe
        page_data = crawl_page(driver)
        page_df = pd.DataFrame(
            page_data,
            columns = df_columns,
            index = [get_unique_id(link) for link in page_data['link']]
            )
        site_df = site_df.append(page_df)
        ut.progress(f"Page {page_count} crawled and saved in dataframe.")
    return site_df

def get_unique_id(url):
    """
    Unique ID for each warning letter

    Parameters
    ----------
    url : String
        URL of the warning letter

    Returns
    -------
    String
        Part of the URL after the last "/"

    """
    return re.findall(r"/([a-z0-9\-]*)$", url)[0]

def save_data(df, db_connection):
    """
    Write dataframe to SQL database
    Parameters
    ----------
    df : dataframe
    db_connection : database connection

    """
    try:
        connection = db_connection.connect()
        # empty transition 'temptable' table
        connection.execute("TRUNCATE temptable")
        # write result to 'temptable' table
        df.to_sql('temptable', db_connection, if_exists ='append', index_label = 'id')
        # use INSERT IGNORE to just skip already existing letters in the 'list' table
        connection.execute("INSERT IGNORE INTO list SELECT * FROM temptable")
        connection.close()
    except Exception as e:
        ut.error("Failed to write dataframe to database.")
        ut.progress(f"Detailed error:\n{e}")
        return 0
    else:
        ut.progress("Dataframe written to database.")
        return 1