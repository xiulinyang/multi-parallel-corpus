import pandas as pd
from collections import Counter, defaultdict
en_data = pd.read_csv('/Users/xiulinyang/Desktop/TODO/en_ar.tsv', sep='\t').to_dict(orient ='records')
sources = defaultdict(int)
sources_overlap = defaultdict(int)
for data in en_data:
    source = data['source'].split('&')[0]
    sources[source]+=len(data['en'].split())
    sources_overlap[source]+=1

print(sources)
print(sources_overlap)