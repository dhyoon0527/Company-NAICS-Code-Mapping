import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

#Request URL
page = requests.get("http://www.muncie.com/Site-Selection-Data/Industrial-Directory.aspx?SeeAll=True")

#Fetch webpage
soup = BeautifulSoup(page.content,"html.parser")

company_list = []
naics_list = []
    
for hlink in soup.find_all("div",{"class": "CompanySearchResultTitle col-md-12"}):
    company_list.append(hlink.text)
    
for naics in soup.find_all("div",{'class': "col-md-4"}):
    if naics.get_text().strip()[:7] == 'Primary':
        naics_list.append(naics.get_text().strip().splitlines()[0][24:28])  

df = pd.DataFrame(list(zip(company_list, naics_list)), columns =['Company Name', 'NAICS Code'])
df.tail()
