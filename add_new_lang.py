import subprocess
import os
from pathlib import Path
from tqdm import tqdm
LANG='it'
LANG_NUM=10
EN_ALIGN = 'en9.txt'
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
            'bible-uedin': ['bible',LANG]
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
    initial_lang = set(read_lines(en_p))
    new_en = []
    for k, v in corpora.items():
        file_path = f'{v[0]}/{lang}_en.txt'
        lang_en = read_lines(file_path)
        for en_sent in lang_en:
            if en_sent in initial_lang:
                new_en.append(en_sent)

    new_en = list(set(new_en))
    print(len(new_en))
    initial_lang = [x.strip() for x in new_en]
    print(sum([len(x.split()) for x in new_en]))
    with open(f'en{LANG_NUM}.txt', 'w') as enlang:
        enlang.write('\n'.join(new_en))
    return initial_lang

def main():


    # for corpus, tdir in corpora.items():
    #     cmd = [
    #         "opus_get",
    #         "-s", "en",
    #         "-t", tdir[1],
    #         "-d", corpus,
    #         "-p", "moses",
    #         "-dl", tdir[0],
    #         "-r", 'latest',
    #     ]
    #
    #     subprocess.run(cmd, check=True)
    #     subprocess.run("yes | unzip '*.zip'", shell=True, cwd=tdir[0])
    #     subprocess.run("rm -f *.zip", shell=True, cwd=tdir[0])
    #     src_en = f"{tdir[0]}/{corpus}.en-{tdir[1]}.en"
    #     dst_en = f"{tdir[0]}/{LANG}_en.txt"
    #
    #     src_lang = f"{tdir[0]}/{corpus}.en-{tdir[1]}.{tdir[1]}"
    #     dst_lang = f"{tdir[0]}/{LANG}.txt"
    #     os.rename(src_en, dst_en)
    #     os.rename(src_lang, dst_lang)

    find_overlap(corpora, LANG, EN_ALIGN)

if __name__ == '__main__':
    main()

