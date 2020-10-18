#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 20:33:03 2020

@author: joachim nuytttens
"""

import utility as ut
import pandas as pd
import sqlalchemy
import re
import nltk
from nltk.corpus import PlaintextCorpusReader

def get_letter_list(db_connection, year, office):
    """
    Load data of letters from database to dataframe.

    Parameters
    ----------
    db_connection
    year: list
        a list of years to include in the query
    office: list
        a list of offices to include in the query

    Returns
    -------
    Dataframe with all letters loaded from database

    """
    # compose query
    query = f"WHERE YEAR(issued) IN ({', '.join(year)}) AND office REGEXP '{'|'.join(office)}'"
    
    # execute query and load to dataframe
    try:
        connection = db_connection.connect()
        df = pd.read_sql(f"SELECT * FROM list {query};", connection)
    except Exception as e:
        ut.error("Failed to retrieve dataframe from database.")
        ut.progress(f"Detailed error:\n{e}")
        return 0
    else:
        #ut.progress("Data retrieved from database.")
        return df


def build_corpus(df, folder):
    """
    Build corpus from dataframe and texts on folder

    Parameters
    ----------
    df : dataframe
        with letters loaded from database
    folder : string
        path to folder in which the warning letters are stored

    Returns
    -------
    wordlists : nltk.corpus.reader.plaintext.PlaintextCorpusReader

    """
    # compose list of files
    file_list = [id + '.txt' for id in df['id'].tolist()]
    # put in corpus
    wordlists = PlaintextCorpusReader(folder, file_list)
    return wordlists

def get_cfr_refs(wordlist, section = None):
    """
    Used to find and return a list of unique CFR references in a list of words
    This function is to be used on one file / warning letter

    Parameters
    ----------
    wordlist : list
        a list of words
    section : string
        210, 211, 800 etc. to query only observations of specific sections in 21CFR

    Returns
    -------
    list
        a list of unique CRF references

    """
    # get short lists of 8 elements around occurences of "CFR"
    CFR_refs = [''.join(wordlist[i-1:i+7]) for i in range(len(wordlist)) if wordlist[i] == "CFR"]
    # within each of the 8 element lists search based on regular expression
    # compile 'section' part of regex based on section argument
    if section:
        resect = f"21CFR?{section}"
    else:
        resect = "21CFR[Part]?[2-9]{1}[0-9]{1,2}"
    shortlist = [re.search(resect + "\.[0-9]{1,3}(\(\w\))?", i) for i in CFR_refs]
    # return list of unique CFR references for each file, we do no want to count doubles in same file
    # exclude entries which are "None"
    return list(set([i.group(0) for i in shortlist if i != None]))

def get_cfr_refs_corpus(corpus, section = None):
    """
    Used to find and return a list of unique CRF references in a corpus
    This function is to be used on a complete corpus

    Parameters
    ----------
    corpus : nltk.corpus.reader.plaintext.PlaintextCorpusReader
        corpus containing warning letters

    Returns
    -------
    cfr_refs : list
        list of CFR references over complete corpus
    cfr_letter_refs : panda series
        CFR references per letter (identified by corpus fileid)

    """
    cfr_refs = []
    cfr_letter_refs = pd.Series()
    # loop over warning letters and extend the list with CFR refs and the
    # panda series with cfr refs per letter
    for fileid in corpus.fileids():
        cfr_list = get_cfr_refs(corpus.words(fileid), section)
        cfr_refs.extend(cfr_list)
        cfr_letter_refs[fileid] = cfr_list
    return cfr_refs, cfr_letter_refs


def get_freq_year(sql_connection, year, office, section = None):
    """
    Find frequency distribution of CFR references per year

    Parameters
    ----------
    sql_connection
        a list of years to include in the query
    office: list
        a list of offices to include in the query

    Returns
    -------
    nltk freqdist
        frequency distribution CFR references quantity

    """
    df = get_letter_list(sql_connection, year, office)
    corpus = build_corpus(df, 'letters')
    cfr_refs, cfr_letter_refs = get_cfr_refs_corpus(corpus, section)
    return nltk.FreqDist(cfr_refs)


def get_cfr_letters_corpus(sql_connection, year, office, ref):
    """
    Used to find and return a list of letter ID's in a corpus in which a
    certain reference occurs.

    Parameters
    ----------
    corpus : nltk.corpus.reader.plaintext.PlaintextCorpusReader
        corpus containing warning letters
    reference : CFR reference to look for

    Returns
    -------
    letter_refs : list
        list of letters in which CFR reference occurs

    """
    letter_refs = []
    # get letter info from database
    df = get_letter_list(sql_connection, year, office)
    # load letters into corpus
    corpus = build_corpus(df, 'letters')
    # get dataframe with crf refs per letter
    cfr_refs, cfr_letter_refs = get_cfr_refs_corpus(corpus)
    # add references of letters with 'ref' into list
    for i in cfr_letter_refs.iteritems():
        if i[1].count(ref):
            letter_refs.append(i[0])
    return letter_refs