import pandas as pd
from pathlib import Path
zh = pd.read_csv('cleaned_parallel/en_zh.tsv', sep='\t').to_dict(orient='records')
en = list(set([x['en'] for x in zh]))
print(len(en), sum([len(x.split()) for x in en]))
with open('en8.txt', 'w') as f:
    f.write('\n'.join(en))