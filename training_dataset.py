import csv
import pandas as pd
import re
import collections
from collections import Counter
from collections import defaultdict
import os
import time
import sys

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.stem import WordNetLemmatizer 

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

from data_web_scraping import *
from data_pdf_parsing import *

df = pd.concat([web_df, pdf_df], ignore_index=True)

'''
Uncomment this to train with your own data set

# For .txt file (for .csv file, use Pandas read_csv)
with open('~/your_own_data_set.txt', 'r') as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    d = list(reader)
df = pd.DataFrame(d[1:], columns=['client_name','industry_driver_naics'])
'''

df.columns = ['client_name', 'industry_driver_naics']

df = df.apply(lambda x: x.astype(str).str.lower())

df['client_name'] = df['client_name'].map(lambda x: re.sub(r'[^A-Za-z ]','',x))

xls = pd.ExcelFile('Excluding.xlsx')

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

df_NAICS_desc = pd.read_excel(xls, '2017 NAICS Description')
print("All data loaded...")

df_NAICS_desc.columns = ['naics', 'naics description']
df_NAICS_desc = df_NAICS_desc.apply(lambda x: x.astype(str).str.lower())

list_naics_desc = df_NAICS_desc['naics description'].tolist()

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

from flashtext import KeywordProcessor

start_time = time.time() # Timer Start

str_clients = ", ".join(list_clients) 

keyword_processor = KeywordProcessor()

keyword_names = list_removals
clean_names = [' '] * len(keyword_names)

for keyword_name, clean_name in zip(keyword_names, clean_names):
    keyword_processor.add_keyword(keyword_name, clean_name)

clean_str_clients = keyword_processor.replace_keywords(str_clients)
clean_str_clients = re.sub(" +" , " ", clean_str_clients)

print("\n","Client name cleaning finished...")

list_clients = clean_str_clients.split(", ")

cleaned_list_clients = [' '.join(set([lemmatizer.lemmatize(word) for word in sentence.split(" ") 
                          if len(lemmatizer.lemmatize(word))>2 or word in list_reinclude]))
                        for sentence in list_clients] 

#Uncomment this block to create normal version dataset
#cleaned_list_clients = [' '.join(set([word for word in sentence.split(" ") 
#                          if len(word)>2 or word in list_reinclude]))
#                        for sentence in list_clients] 

list_tk_clients = []
list_tk_industries = []

for clientName, ind in zip(cleaned_list_clients, list_industries):
    for word in clientName.split():
        list_tk_clients.append(word)
        list_tk_industries.append(ind)
        
df_tk_word_ind = pd.DataFrame({'word': list_tk_clients, 'ind': list_tk_industries})

word_dict = {}
word_dict = defaultdict(lambda: 0, word_dict)

for word in list(set(list_tk_clients)):
    word_dict[word]
    
list_ind = []
list_word = []
list_word_freq = []
list_document_freq = []

for ind in list(set(list_industries)):
    matching_words = (df_tk_word_ind.loc[df_tk_word_ind['ind'] == ind])['word'].tolist()

    for word in list(set(matching_words)):
        word_dict[word] += 1
        
    counter=collections.Counter(matching_words)

    list_ind.extend([ind] * len(counter.keys()))
    list_word.extend(counter.keys())
    list_word_freq.extend(counter.values())

print("\n","Counting finished. Ready to export!")
  
# Word count across the document     
for word in list_word:
    list_document_freq.extend([word_dict.get(word)])
    
final_df = pd.DataFrame(list(zip(list_ind, list_word,list_word_freq,list_document_freq)), 
              columns =['naics', 'name','freq','freq_document']) 
final_df = final_df.sort_values(by = ['naics','freq'], ascending=[True, False]).reset_index(drop=True)

final_df.to_csv('industry_keywords.csv', encoding = 'utf-8', index = False)

print("\n","Running over! Final document will be located in your local directory")
