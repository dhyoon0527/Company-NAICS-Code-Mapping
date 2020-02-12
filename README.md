# Company-NAICS-Code-Matching

## Overview
> This project will help to assign incoming company name with no industry code (NAICS) with predicted NAICS code. A NAICS code is a industrial classification within the North American Industry Classification System, developed by Federal Statistical Agencies for collection, analysis and publication purposes.

## Requirement
Language: Python 3.6.X

Data: Two options to train for TF-IDF model
> OptionYour own data for training dataset(company names with NAICS codes) and test dataset(only company names). For validation purposes, you can split your data with certain ratio to check the model performance

## Abstract
> There will be two parts of python script. First one is about modeling. We're going to implement TF-IDF to rank the importance of partitioned words and apply it to tokenized incoming words (company name). Second script is a training set for the model, with the historical data (it should be reliable source) to document frequency of tokenized word of company name with its NAICS code. 
