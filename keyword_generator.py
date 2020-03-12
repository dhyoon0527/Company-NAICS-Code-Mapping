import csv
import pandas as pd
import re
import collections
from collections import Counter
from collections import defaultdict
from flashtext import KeywordProcessor
import os
import time

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer 
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

from data.data_web_scraping import *
from data.data_pdf_parsing import *

'''
Uncomment this to train with your own data set

# For .txt file (for .csv file, use Pandas read_csv)
with open('~/your_own_data_set.txt', 'r') as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    d = list(reader)
df = pd.DataFrame(d[1:], columns=['client_name','industry_driver_naics'])
'''

df = pd.concat([web_df, pdf_df], ignore_index=True) # Using open-source data

df.columns = ['client_name', 'industry_driver_naics']

# Add Official NAICS Description File into df
xls = pd.ExcelFile('/Users/dyoon/GitHub/data/Excluding Words.xlsx')

df_NAICS_desc = pd.read_excel(xls, '2017 NAICS Description')
df_NAICS_desc.columns = ['client_name', 'industry_driver_naics']

df = df.append(df_NAICS_desc, ignore_index=True)

df = df.apply(lambda x: x.astype(str).str.lower())
df['client_name'] = df['client_name'].map(lambda x: re.sub(r'[^A-Za-z ]','',x))

## Client Name Filters ##
df_cleanName = pd.read_excel(xls, 'People Names', header=None)
list_cleanName = df_cleanName[0].tolist()

list_removals = [x for x in list_cleanName if x != 'nan']

adj_removals = pd.read_excel(xls, 'Adjectives', header = None)
list_adj = adj_removals.iloc[:,0].tolist()

list_removals += list_adj

df_city = pd.read_excel(xls, 'US State.City.County')

list_city = df_city['City'].tolist()
list_city = [city.lower() for city in list_city if str(city) != 'nan']

list_state = df_city['State'].tolist()
list_state = [state.lower() for state in list_state if str(state) != 'nan']

list_county = df_city['County'].tolist()
list_county = [county.lower() for county in list_county if str(county) != 'nan']

list_removals += (list_county + list_state + list_city)

list_removals += ['zero','one','two','three','four','five','six','seven','eight','nine','ten',
                  'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen',
                  'twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety','hundred',
                  'bill','bro','top','choice','jak',
                  'north','south','east','west','southeast','southwest','northeast','northwest','southern',
                  'northern','eastern','western','southeastern','southwestern'
                  'son','ave','nyc','myers','cal','tex','fun','luci',
                  'monday','mon','tuesday','tue','wednesday','wed','thursday','thu','friday','fri'
                  'january','jan','february','feb','march','mar','april','apr','may','june','july','august',
                  'aug','septempber','sep','october','oct','novemember','nov','december','dec']
                  
list_removals += ['inc','co','llc','ltd','company','industry','dba','llp',
                  'enterprise','blvd','street','enterprise','corporation','corp']

stopwords = nltk.corpus.stopwords.words('english')

list_removals += stopwords

print("All data loaded...","\n")

list_naics_desc = df_NAICS_desc['industry_driver_naics'].tolist()

list_adj_reinclude = [adj for adj in list_adj if adj in list_naics_desc]
list_people_name_reinclude = [ppl for ppl in list_cleanName if ppl in list_naics_desc]

list_reinclude = (list_adj_reinclude + list_people_name_reinclude)

list_reinclude += ['university','petroleum','union','church','christ','home','burger',
                      'upchurch','school','supply','electric','rock','living','art','md',
                      'dmd','isd','od','pc','pa','do','bbbs','condo']
                      
list_removals = [x for x in list_removals if x not in list_reinclude]
list_removals = list(set(list_removals)) # unique sets

list_clients = df[df.columns[0]].tolist()
list_industries = df[df.columns[1]].tolist()

str_clients = ", ".join(list_clients) 

keyword_processor = KeywordProcessor()

keyword_names = list_removals
clean_names = [' '] * len(keyword_names)

for keyword_name, clean_name in zip(keyword_names, clean_names):
    keyword_processor.add_keyword(keyword_name, clean_name)

clean_str_clients = keyword_processor.replace_keywords(str_clients)
clean_str_clients = re.sub(" +" , " ", clean_str_clients)

print("Client name cleaning finished...","\n")

list_clients = clean_str_clients.split(", ")

cleaned_list_clients = [' '.join(set([lemmatizer.lemmatize(word) for word in sentence.split(" ") 
                          if len(lemmatizer.lemmatize(word))>2 or word in list_reinclude]))
                        for sentence in list_clients] 

list_tk_clients = []
list_tk_industries = []

for clientName, ind in zip(cleaned_list_clients, list_industries):
    for word in clientName.split():
        list_tk_clients.append(word)
        list_tk_industries.append(ind)
        
df_tk_word_ind = pd.DataFrame({'term': list_tk_clients, 'naics': list_tk_industries})

keyword_df = df_tk_word_ind.groupby('naics').agg({'term': ' '.join}).reset_index()
keyword_df.tail()

print("Keyword dataframe is ready!")