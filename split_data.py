import os
from pathlib import Path
from random import sample, shuffle
from tqdm import tqdm
import random
random.seed(42)
langs = ['zh', 'tr', 'ar', 'de', 'fi', 'ko','fr','pl','ru' ]
data_split = 'parallel10'
# langs = ['zh', 'ar']
# data_split = 'parallel3'
parall_data_path = 'multilingual_parallel'
en = Path(f'{parall_data_path}/ar_en.txt').read_text().strip().split('\n')

shuffle(en)
test = sample(en, 40000)
remain = list(set(en) - set(test))
dev = sample(remain, 10000)
blocked = set(test) | set(dev)
train = [x for x in en if x not in blocked]
#
# train100 = []
# target_words = 100_000_000
# total_words = 0
#
# for sent in train:
#     n_words = len(sent.split())
#     if total_words + n_words > target_words:
#         break
#     train100.append(sent)
#     total_words += n_words
#
# print(f"Selected {len(train100):,} sentences, {total_words/1_000_000:.1f}M words")


print('finish sampling english data')

os.makedirs(data_split, exist_ok=True)
en_train_path = f'{data_split}/EN/train/'
en_dev_path = f'{data_split}/EN/dev/'
en_test_path = f'{data_split}/EN/test/'
# en_train100_path = f'parallel3_100/EN/train/'
os.makedirs(en_train_path, exist_ok=True)
os.makedirs(en_dev_path, exist_ok=True)
os.makedirs(en_test_path, exist_ok=True)
# os.makedirs(en_train100_path, exist_ok=True)
with open(f'{data_split}/EN/train/EN.txt', 'w') as en_t, open(f'{data_split}/EN/dev/EN.txt', 'w') as en_d, open(f'{data_split}/EN/test/EN.txt', 'w') as en_e: #,open(f'{en_train100_path}/EN.txt', 'w') as en_t100
    t_en ='\n'.join(train)
    d_en ='\n'.join(dev)
    tes_en ='\n'.join(test)
    # en_100 = '\n'.join(train100)

    en_t.write(t_en)
    en_d.write(d_en)
    en_e.write(tes_en)
    # en_t100.write(en_100)
    train_len = sum(len(x.split()) for x in train)
    dev_len = sum(len(x.split()) for x in dev)
    test_len = sum(len(x.split()) for x in test)
    # train_100_len = sum(len(x.split()) for x in train100)

    print('EN')
    print(train_len, dev_len, test_len)


for lang in tqdm(langs):
    pair_en = Path(f'{parall_data_path}/{lang}_en.txt').read_text().strip().split('\n')
    pair_lang = Path(f'{parall_data_path}/{lang}.txt').read_text().strip().split('\n')
    print(len(pair_en), len(pair_lang))
    assert len(pair_en) == len(pair_lang)
    en_lang_pair ={x:y for x, y in zip(pair_en, pair_lang)}
    lang_name = lang.upper()
    train_path = f'{data_split}/{lang_name}/train'
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


    with open(f'{train_path}/{lang_name}.txt', 'w') as f_train, open(f'{train_path}/{lang_name}.txt', 'w') as f_dev, open(f'{train_path}/{lang_name}.txt', 'w') as f_test:
        train_text = '\n'.join(train_lang)
        dev_text = '\n'.join(dev_lang)
        test_text = '\n'.join(test_lang)
        f_train.write(train_text)
        f_dev.write(dev_text)
        f_test.write(test_text)
