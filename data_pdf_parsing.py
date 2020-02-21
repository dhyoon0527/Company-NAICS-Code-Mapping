import PyPDF2 
import pandas as pd
import collections

pdfFileObj = open('/Users/dyoon/Documents/Industry Mapping/All_Facilities_Alpha.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

company_list = []

for pageNum in range(4,pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    company_list.extend([x for x in pageObj.extractText().splitlines() if len(x) > 1])

space_words = {i:company_list[i]+company_list[i+1] for i in range(0,len(company_list)) 
               if company_list[i].endswith(" ")}
non_space_words = {i:company_list[i] for i in range(0,len(company_list)-1) 
               if company_list[i].endswith(" ") == False and
                  company_list[i-1].endswith(" ") == False}

merged_words = z = {**space_words, **non_space_words}
merged_words = collections.OrderedDict(sorted(merged_words.items()))

cleaned_words = list(merged_words.values())

pdf_company_list = [cleaned_words[i] for i in range(0,len(cleaned_words)-3) if "NAICS" in cleaned_words[i+2]  ]# if "NAICS" not in cleaned_words[i] and "KY" not in cleaned_words[i]]

pdf_naics_list = [naics for naics in cleaned_words if "NAICS" in naics]
pdf_naics_list = [' '.join(w for w in p.split() if w not in "NAICS: ")[:4] for p in pdf_naics_list] #Parse only first NAICS code

pdf_df = pd.DataFrame(list(zip(pdf_company_list, pdf_naics_list)), columns =['Company Name', 'NAICS Code'])
