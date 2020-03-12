import cloudpickle
from keyword_generator import *

def clean_name(company_name):
	company_name = re.sub(r'[^A-Za-z ]',' ',company_name)
	company_name = company_name.lower()
	
	keyword_processor = KeywordProcessor()
	
	keyword_names = list_removals
	clean_names = [' '] * len(keyword_names)
	
	for keyword_name, clean_name in zip(keyword_names, clean_names):
		keyword_processor.add_keyword(keyword_name, clean_name)
	
	clean_company = keyword_processor.replace_keywords(company_name)
	clean_company = re.sub(" +" , " ", clean_company)
	clean_company = clean_company.strip()

	return clean_company
	
def naics_pred(company_name):
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.metrics.pairwise import linear_kernel

	assert type(company_name) == str

	company_name = clean_name(company_name)
	
	list_term = list(keyword_df['term'].values)
	list_term.insert(0,company_name)
		
	tfidf = TfidfVectorizer().fit_transform(list_term)
	
	cos_sim = linear_kernel(tfidf[0:1], tfidf).flatten()
	top_match = cos_sim.argsort()[::-1][1]
	top_match_df = keyword_df[keyword_df['term'] == list_term[top_match]]
	
	return top_match_df['naics'].values[0]

cloudpickle.dump(naics_pred, open('pickles/model.pkl','wb'))
