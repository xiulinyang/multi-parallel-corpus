import subprocess
import os
from pathlib import Path
from tqdm import tqdm
LANG='ja'
LANG_NUM=9
EN_ALIGN = 'en8.txt'
corpora = {'OpenSubtitles': ['opensubs', LANG],
           'LinguaTools-WikiTitles': ['wiki', LANG],
           'NeuLab-TedTalks': ['neulab_ted', LANG],
           'TED2020': ['ted2020', LANG],
           # 'TED2013': 'ted2013',
           'Tanzil': ['tanzil', LANG],
           'Tatoeba': ['tatoeba', LANG],
           'GNOME': ['gnome', LANG],
           'QED': ['qed', LANG],
           'Ubuntu': ['ubuntu', LANG],
           'KDE4': ['kde4', LANG],
           'GlobalVoices': ['gv', LANG],
           'tldr-pages': ['tldr', LANG],
            'bible-uedin': ['bible','jap']
           }

def read_lines(file_path):
    '''
    :param file_path: the path of each document
    :return: sentence for each line in the file
    '''

    return [x.strip() for x in Path(file_path).read_text().strip().split('\n')]



def find_overlap(corpora, lang, en_p):
    '''
    :param file_paths: the paths where the English-centered parallel corpora are located.
    :return: the overlap English sentences across all English-centered parallel corpora.
    '''
    initial_lang = read_lines(en_p)
    for k, v in corpora.items():
        file_path = f'{v}/{lang}_en.txt'
        lang_en = read_lines(file_path)
        initial_lang &= set(lang_en)
    print(len(initial_lang))
    initial_lang = [x.strip() for x in initial_lang]
    print(sum([len(x.split()) for x in initial_lang]))
    with open(f'en{LANG_NUM}.txt', 'w') as enlang:
        enlang.write('\n'.join(initial_lang))
    return initial_lang

def main():


    for corpus, tdir in corpora.items():
        cmd = [
            "opus_get",
            "-s", "en",
            "-t", tdir[1],
            "-d", corpus,
            "-p", "moses",
            "-dl", tdir[0],
            "-r", 'latest',
        ]

        subprocess.run(cmd, check=True)
        subprocess.run("yes | unzip '*.zip'", shell=True, cwd=tdir)
        subprocess.run("rm -f *.zip", shell=True, cwd=tdir)
        src_en = f"{tdir}/{corpus}.en-{tdir[1]}.en"
        dst_en = f"{tdir}/{LANG}_en.txt"

        src_lang = f"{tdir}/{corpus}.en-{tdir[1]}.{tdir[1]}"
        dst_lang = f"{tdir}/{LANG}.txt"
        os.rename(src_en, dst_en)
        os.rename(src_lang, dst_lang)

    find_overlap(corpora, LANG, EN_ALIGN)

if __name__ == '__main__':
    main()

