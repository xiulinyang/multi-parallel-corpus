'''
This script is used to build multilingual parallel corpora.
So far, the script supports 8 languages, and it is easy to add more.
'''

import os
from pathlib import Path
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser('compile data')
parser.add_argument('-t', '--target_dir', help='Generated data directory', required=True)
parser.add_argument('-s', '--source_dir', help='Source data directory', required=True)

args = parser.parse_args()
source_dir = args.source_dir
target_dir = args.target_dir


lang_paths = {
'ar': {
       'en': f'{source_dir}/ar_en.txt',
       'ar': f'{source_dir}/ar.txt'
  },
   # 'de': {
   #     'en': f'{source_dir}/de_en.txt',
   #     'de': f'{source_dir}/de.txt'
   # },
   #  'ru': {
   #      'en': f'{source_dir}/ru_en.txt',
   #      'ru': f'{source_dir}/ru.txt'
   #  },
    'zh': {
        'en': f'{source_dir}/zh_en.txt',
        'zh': f'{source_dir}/zh.txt'
    },
   # 'fr': {
   #     'en': f'{source_dir}/fr_en.txt',
   #     'fr': f'{source_dir}/fr.txt'
   # },
   #
   # 'tr': {
   #     'en': f'{source_dir}/tr_en.txt',
   #     'tr': f'{source_dir}/tr.txt'
   # },
   #
   # 'pl': {
   #     'en': f'{source_dir}/pl_en.txt',
   #     'pl': f'{source_dir}/pl.txt'
   # },
   #
   #  'fi': {
   #      'en': f'{source_dir}/fi_en.txt',
   #      'fi': f'{source_dir}/fi.txt'
   #  },
   #
   #  'ko': {
   #      'en': f'{source_dir}/ko_en.txt',
   #      'ko': f'{source_dir}/ko.txt'
   #  },

}

print(lang_paths)
def ensure_directories(path):
    Path(path).mkdir(parents=True, exist_ok=True)

ensure_directories(f'{target_dir}')

def find_overlap(file_paths):
    '''
    :param file_paths: the paths where the English-centered parallel corpora are located.
    :return: the overlap English sentences across all English-centered parallel corpora.
    '''

    initial_lang = set(read_lines(file_paths['zh']['en']))
    for lang in tqdm(file_paths):
        if lang =='zh':
            continue
        try:
            lang_en = read_lines(file_paths[lang]['en'])
            initial_lang &= set(lang_en)
        except FileNotFoundError as e:
            print(e)
            continue

    print(len(initial_lang))
    return initial_lang


def read_lines(file_path):
    '''
    :param file_path: the path of each document
    :return: sentence for each line in the file
    '''

    return [x.strip() for x in Path(file_path).read_text().strip().split('\n')]

def write_lines(file_path, lines):
    '''
    :param file_path: target file path
    :param lines: list of sentences
    :return:
    '''
    with open(file_path, 'w') as f:
        for line in lines:
            line = line.strip()
            f.write(f'{line}\n')


def create_dic(en, other):
    aligned_dic = {}
    for i, sent in enumerate(en):
        aligned_dic[sent] = other[i]
    return aligned_dic


def create_parallel_corpus(overlap_en, file_paths):
    '''
    :param overlap_en:
    :param file_paths:
    :return:
    '''
    overlap_en_list = list(overlap_en)
    for lang in tqdm(file_paths):
        parallel_en =[]
        parallel_lang = []
        en = read_lines(file_paths[lang]['en'])
        lan = read_lines(file_paths[lang][lang])
        assert len(en) == len(lan)
        new_en = []
        new_lan =[]
        for i, sent in tqdm(enumerate(en)):
            if sent in overlap_en:
                if len(sent.strip().split())<3:
                    continue
                # if not len(lan[i].strip()):
                #     continue

                new_en.append(sent)
                new_lan.append(lan[i])
        en_lan = create_dic(new_en, new_lan)
        for en_sent in overlap_en_list:
            target_sent = en_lan.get(en_sent)
            if target_sent is None:
                continue
            parallel_en.append(en_sent)
            parallel_lang.append(target_sent)
        en_words = sum([len(x.split()) for x in parallel_en])
        lang_words = sum([len(x.split()) for x in parallel_lang])
        print(lang, len(parallel_en), len(parallel_lang), en_words, lang_words)
        with open('parallel_stats.tsv', 'a') as p_s:
            p_s.write(f'{source_dir}\t{lang}\t{en_words}\t{lang_words}\t{len(parallel_lang)}\t{len(parallel_en)}\n')
        write_lines(f'{target_dir}/{lang}.txt', parallel_lang)
        write_lines(f'{target_dir}/{lang}_en.txt', parallel_en)


if __name__ == "__main__":
    overlap_en = find_overlap(lang_paths)
    create_parallel_corpus(overlap_en, lang_paths)
