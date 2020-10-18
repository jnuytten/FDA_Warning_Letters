#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 17:09:04 2020

@author: joachim nuyttens
"""

from nltk.corpus import stopwords 

def sent_similarity(sent1, sent2):
    """
    Calculate similarity factor for two sentences. Based on:
        https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/

    Parameters
    ----------
    sent1 : list
        first sentence as list of words
    sent2 : list
        second sentence as list of words

    Returns
    -------
    cosine : float
        similarity factor (cosine) in between 0 and 1, where 1 means identical

    """
    stopws = stopwords.words('english')
    # remove stopwords and keep only one instance of each word
    sent1_set = set([word for word in sent1 if not word in stopws])
    sent2_set = set([word for word in sent2 if not word in stopws])
    # define two vectors
    l1 =[];l2 =[]
    
    # form a set containing keywords of both strings  
    rvector = sent1_set.union(sent2_set)  
    for word in rvector: 
        if word in sent1_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if word in sent2_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
      
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    return cosine

      
def observation_set(sent_list):
    """
    Group observations based on similarity.

    Parameters
    ----------
    sent_list : list
        list of sentences to evaluate

    Returns
    -------
    observations : list
        list of unique observations
    occurences : list
        list of counts associated to each of the unique observations

    """
    # add first sentence to the list of unique observations with count of occurences 1
    observations, occurences = [sent_list[0]], [1]
    # loop over other sentences
    for i in range(1, len(sent_list)):
        # for each sentence loop over unique observations
        for n in range(len(observations)):
            # if similar, do not add but increase count of existing observation
            if sent_similarity(sent_list[i], observations[n]) > 0.8:
                occurences[n] = occurences[n] + 1
                break
        # if not similar, add to list of unique observations
        else:
            observations.append(sent_list[i])
            occurences.append(1)
    return observations, occurences