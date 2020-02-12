# Company-NAICS-Code-Matching

## Getting Started
This project will help to assign input of company name with no industry code (NAICS) with predicted NAICS code, using TF-IDF model with cosine similarity. To train TF-IDF model, a set of training that composed of business names and NAICS codes is needed. After building a model, it will be deployed using Flask.

### Requirements
Language: Python 3.6.X

Data: Two options
1. Bring your own dataset of company names with their NAICS codes 
2. Use built-in data from this repository that I webscraped from Delare County and Kentucky Directory
 
## Abstract for Steps
1. 
> There will be two parts of python script. First one is about modeling. We're going to implement TF-IDF to rank the importance of partitioned words and apply it to tokenized incoming words (company name). Second script is a training set for the model, with the historical data (it should be reliable source) to document frequency of tokenized word of company name with its NAICS code. 




