# Company-NAICS-Matching

## Getting Started
This project will assign company name with no industry code (NAICS) with predicted NAICS code, using TF-IDF model with cosine similarity. To build TF-IDF model, training dataset for business names and NAICS codes are needed. If you have and are confident with your dataset, please use it. In case if you don't have your own dataset, I gathered data through web scraping and pdf parsing from open source.

Once data is ready, keyword_generator.py will wrangle the data into clean (no special characters) and lemmatized version. With this "cleaned" sets, once user types the company name they want to predict, the TF-IDF model will calculate cosine-similiarity with given name and cleaned sets. These sets are grouped by NAICS codes, so that the closest term's NAICS code can be shown as a predicted NAICS code.

### Requirements
Language: Python 3.6.X

Data: Two options
1. Bring your own dataset of company names with their NAICS codes. This would be the most **ideal** option if you (or your company) have massive amount of correctly recorded sets of names with codes. Actually, my current company has 1M+ rows of such data with very high accuracy, but can't share details of data since it's confidential. That's why I introduced the second option
2. Use built-in data from this repository that I gathered using web-scraping from Muncie-Delaware County and Kentucky Directory

### Libaries Used
* Pandas, Numpy, Cloudpickle, Pickle, Flask, FlashText, Collections, Requests

### Application Example
![alt text](https://raw.githubusercontent.com/dhyoon0527/Industry-Classification/Application-Example.png)


### Data Source
* Industrial Directory for Muncie-Delaware County: http://www.muncie.com/Site-Selection-Data/Industrial-Directory.aspx?SeeAll=True
* Kentucky Directory of Business & Industry: http://www.thinkkentucky.com/kyedc/kpdf/All_Facilities_Alpha.pdf

> *All data are used for education purposes*
