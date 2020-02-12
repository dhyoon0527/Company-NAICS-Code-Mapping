# Company-NAICS-Matching

## Getting Started
This project will assign input of company name with no industry code (NAICS) with predicted NAICS code, using TF-IDF model with cosine similarity. To train TF-IDF model, a set of training, composed of business names and NAICS codes, is needed. After building a model, it will be deployed using Flask.

### Requirements
Language: Python 3.6.X

Data: Two options
1. Bring your own dataset of company names with their NAICS codes. This would be the most **ideal** option if you (or your company) have massive amount of correctly recorded sets of names with codes. Actually, my current company has 1M+ rows of such data with very high accuracy, but can't share details of data since it's confidential. That's why I introduced the second option
2. Use built-in data from this repository that I gathered using web-scraping from Muncie-Delaware County and Kentucky Directory


### Data Source
* Industrial Directory for Muncie-Delaware County: http://www.muncie.com/Site-Selection-Data/Industrial-Directory.aspx?SeeAll=True
* Kentucky Directory of Business & Industry: http://www.thinkkentucky.com/kyedc/kpdf/All_Facilities_Alpha.pdf

> *All data used are for education purposes*
