import pandas as pd
from pathlib import Path
import random

from pandas import DataFrame

zh = pd.read_csv('cleaned_parallel/en_zh.tsv', sep='\t').to_dict(orient='records')
en = list(set([x['en'] for x in zh]))
with open('en_zh_judgements.tsv', 'w') as s:
    en_sample = random.sample(en, 500)
    DataFrame(en_sample).to_csv('en_zh_judgements.tsv', sep='\t', index=False)
# print(len(en), sum([len(x.split()) for x in en]))
# with open('en8.txt', 'w') as f:
#     f.write('\n'.join(en))