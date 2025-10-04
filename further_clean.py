import opencc
import pandas as pd
import re
from tqdm import tqdm
def clean_text(text):
    invisible_chars = [
        "\u200e",  # LRM (Left-to-Right Mark)
        "\u200f",  # RLM (Right-to-Left Mark)
        "\u202a",  # LRE
        "\u202b",  # RLE
        "\u202c",  # PDF
        "\u202d",  # LRO
        "\u202e",  # RLO
        "\ufeff",  # BOM
        "\u2060",  # WJ (Word Joiner)
        "\u200b",  # ZWSP (Zero Width Space)
        "\u200c",  # ZWNJ
        "\u200d",  # ZWJ
    ]
    pattern = "[" + "".join(invisible_chars) + "]"
    text = text.replace("\u00a0", " ")
    return re.sub(pattern, "", text)

converter = opencc.OpenCC('t2s.json')
# langs = ['zh', 'tr', 'ar', 'de', 'fi', 'ko','fr','pl','ru' ]
langs = ['zh', 'ar']
for lang in tqdm(langs):
    t_lang = []
    en_lang = []
    tgt_lang = pd.read_csv(f'cleaned_3/en_{lang}.tsv', sep='\t').to_dict(orient='records')
    with (open(f'multilingual_data/{lang}.txt', 'w') as f,
          open(f'multilingual_data/{lang}_en.txt', 'w') as e):
        for tgt_text in tgt_lang:
            trans = tgt_text['trans']
            if lang == 'zh':
                trans = converter.convert(trans)
                if tgt_text['source'] == 'bible':  # bible text add space between characters so we will remove the space
                    trans = ''.join(trans.split())
            trans = clean_text(trans)
            trans = trans.replace('lrm;', '')
            trans = trans.replace('lrm- ;', '')
            trans = re.sub(r'\{.*?\}', '', trans)
            trans = trans.strip()
            if '{' in trans:
                continue
            f.write(trans + '\n')
            e.write(tgt_text['en']+'\n')
            t_lang.append(trans)
            en_lang.append(tgt_text['en'])
    assert len(t_lang) == len(en_lang)