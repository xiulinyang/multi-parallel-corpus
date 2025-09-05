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
    'de': {
        'en': f'{source_dir}/de_en.txt',
        'de': f'{source_dir}/de.txt'
    },
    'ru': {
        'en': f'{source_dir}/ru_en.txt',
        'ru': f'{source_dir}/ru.txt'
    },
    'zh': {
        'en': f'{source_dir}/zh_en.txt',
        'zh': f'{source_dir}/zh.txt'
    },
    'fr': {
        'en': f'{source_dir}/fr_en.txt',
        'fr': f'{source_dir}/fr.txt'
    },
    'nl': {
        'en': f'{source_dir}/nl_en.txt',
        'nl': f'{source_dir}/nl.txt'
    },
    'tr': {
        'en': f'{source_dir}/tr_en.txt',
        'tr': f'{source_dir}/tr.txt'
    },
    'es': {
        'en': f'{source_dir}/es_en.txt',
        'es': f'{source_dir}/es.txt'
    },
    'ar': {
        'en': f'{source_dir}/ar_en.txt',
        'ar': f'{source_dir}/ar.txt'
    },
    'it': {
        'en': f'{source_dir}/it_en.txt',
        'it': f'{source_dir}/it.txt'
    },
    'pl': {
        'en': f'{source_dir}/pl_en.txt',
        'pl': f'{source_dir}/pl.txt'
    }
}

def ensure_directories(path):
    Path(path).mkdir(parents=True, exist_ok=True)

ensure_directories(f'{target_dir}')

test  = Path(f'{target_dir}/de_en.txt').read_text().strip().split('\n')

def find_overlap(file_paths):
    '''
    :param file_paths: the paths where the English-centered parallel corpora are located.
    :return: the overlap English sentences across all English-centered parallel corpora.
    '''

    initial_lang = set(read_lines(file_paths['de']['en']))
    for lang in tqdm(file_paths):
        if lang =='de':
            continue

        lang_en = read_lines(file_paths[lang]['en'])
        initial_lang &= set(lang_en)

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
    for lang in tqdm(file_paths):
        parallel_en =[]
        parallel_lang = []
        en = read_lines(file_paths[lang]['en'])
        lan = read_lines(file_paths[lang][lang])
        new_en = []
        new_lan =[]
        for i, sent in tqdm(enumerate(en)):
            if sent not in test:
                new_en.append(sent)
                new_lan.append(lan[i])
        en_lan = create_dic(new_en, new_lan)
        for en_sent in overlap_en:
            if en_sent in tqdm(en_lan):
                parallel_en.append(en_sent)
                parallel_lang.append(en_lan[en_sent])
        print(len(parallel_en), len(parallel_lang))
        write_lines(f'{target_dir}/{lang}.txt', parallel_lang)
        write_lines(f'{target_dir}/{lang}_en.txt', parallel_en)


if __name__ == "__main__":
    overlap_en = find_overlap(lang_paths)
    create_parallel_corpus(overlap_en, lang_paths)
