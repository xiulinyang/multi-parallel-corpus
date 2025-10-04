from pathlib import Path
from collections import Counter
from tqdm import tqdm
import numpy as np
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt

VIS=False
SOR=True

#-------------------
# visualize length distribution of each language
#--------------------
if VIS:
    plt.style.use("seaborn-v0_8")
    langs = ['zh', 'ko', 'ar','de','pl','ru','tr','ar_en','fi','fr']
    # colors = plt.cm.gist_stern(np.linspace(0, 1, len(langs)))
    colors = ['#9e0142', '#d53e4f','#f46d43', '#fdae61', '#fee08b',
              '#e6f598','#abdda4','#66c2a5','#3288bd','#5e4fa2']

    lang_full = {
        'zh': 'Chinese',
        'tr': 'Turkish',
        'ar': 'Arabic',
        'de': 'German',
        'fi': 'Finnish',
        'ko': 'Korean',
        'fr': 'French',
        'pl': 'Polish',
        'ru': 'Russian',
        'ar_en': 'English'
    }


    max_len = 0
    all_length_distribution = []
    for lang, color in tqdm(zip(langs, colors)):
        print(lang)
        text = Path(f'multilingual_parallel/{lang}.txt').read_text().strip().split('\n')
        length = [min(len(x), 200) for x in text]
        dist = Counter(length)
        lengths, freqs = zip(*sorted(dist.items()))
        plt.plot(lengths, freqs, label=lang_full.get(lang, lang), color=color, alpha=0.6)
        # plt.fill_between(lengths, freqs, color=color, alpha=0.1)
        max_len = max(max_len, max(lengths))

    plt.xlabel("Sentence length (number of characters)", fontsize=20)
    plt.ylabel("Frequency", fontsize=20)
    plt.title("Sentence length distribution by language", fontsize=20)
    plt.legend(title="Language", fontsize=15)
    plt.xlim(0, max_len)
    plt.tight_layout()
    plt.savefig('distribution.pdf')
    plt.show()

#-------------------
#get source distribution (the input should be one of the tsv files generated after merge_files.py
#--------------------
if SOR:
    en_data = pd.read_csv('cleaned/en_ar.tsv', sep='\t').to_dict(orient ='records')
    sources = defaultdict(int)
    sources_overlap = defaultdict(int)
    for data in en_data:
        source = data['source'].split('&')[0]
        sources[source]+=len(data['en'].split())
        sources_overlap[source]+=1

    print(sources)
    print(sources_overlap)

