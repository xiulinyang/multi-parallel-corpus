import os
from pathlib import Path
from random import sample, shuffle
from tqdm import tqdm
en = Path('multilingual_parallel/ar_en.txt').read_text().strip().split('\n')
shuffle(en)
test = sample(en, 40000)
dev = sample(en, 10000)
train = [x for x in en if x not in test+dev]
# langs = ['zh', 'tr', 'ar', 'de', 'fi', 'ko','fr','pl','ru' ]
# data_split = 'parallel10'

langs = ['zh', 'tr']
data_split = 'parallel3'

with open(f'{data_split}/EN/train/EN.txt', 'w') as en_t, open(f'{data_split}/EN/dev/EN.txt', 'w') as en_d, open(f'{data_split}/EN/test/EN.txt', 'w') as en_e:
    t_en ='\n'.join(train)
    d_en ='\n'.join(dev)
    tes_en ='\n'.join(test)

    en_t.write(t_en)
    en_d.write(d_en)
    en_e.write(tes_en)
    train_len = sum([len(x.split()) for x in train])
    dev_len = sum([len(x.split()) for x in dev])
    test_len = sum([len(x.split()) for x in test])
    print('EN')
    print(train_len, dev_len, test_len)

os.makedirs(data_split, exist_ok=True)
for lang in tqdm(langs):
    pair_en = Path(f'multilingual_parallel/{lang}_en.txt').read_text().strip().split('\n')
    pair_lang = Path(f'multilingual_parallel/{lang}.txt').read_text().strip().split('\n')
    assert len(pair_en) == len(pair_lang)
    en_lang_pair ={x:y for x, y in zip(pair_en, pair_lang)}
    lang_name = lang.upper()
    train_path = f'{data_split}/{lang_name}/'
    dev_path = f'{data_split}/{lang_name}/dev'
    test_path = f'{data_split}/{lang_name}/test'
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(dev_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    train_lang = [en_lang_pair[x] for x in train]
    dev_lang = [en_lang_pair[x] for x in dev]
    test_lang = [en_lang_pair[x] for x in test]
    print(lang_name)
    print('#sent')
    print(len(train_lang), len(dev_lang), len(test_lang))


    with open(f'{train_path}/{lang_name}.train', 'w') as f_train, open(f'{train_path}/{lang_name}.dev', 'w') as f_dev, open(f'{train_path}/{lang_name}.test', 'w') as f_test:
        train_text = '\n'.join(train_lang)
        dev_text = '\n'.join(dev_lang)
        test_text = '\n'.join(test_lang)
        f_train.write(train_text)
        f_dev.write(dev_text)
        f_test.write(test_text)
