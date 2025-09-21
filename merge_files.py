from glob import glob
from pathlib import Path
parallel_dirs = sorted(glob('*_parallel/'))

langs = ['de', 'fr', 'zh', 'pl', 'ru', 'tr','ar', 'fi', 'ko']
Path("merged").mkdir(exist_ok=True)

def read_lines(file_path):
    '''
    :param file_path: the path of each document
    :return: sentence for each line in the file
    '''
    return [x.strip() for x in Path(file_path).read_text().strip().split('\n')]



for lang in langs:
    merged_en, merged_lang = [], []
    for d in parallel_dirs:
        en_file =  f"{d}/{lang}_en.txt"
        la_file =  f"{d}/{lang}.txt"

        en_lines = read_lines(en_file)
        la_lines = read_lines(la_file)

        if len(en_lines) != len(la_lines):
            raise ValueError(f"Line mismatch in {d} for {lang}: {len(en_lines)} vs {len(la_lines)}")

        merged_en.extend(en_lines)
        merged_lang.extend(la_lines)

    Path(f"merged/{lang}_en.txt").write_text("\n".join(merged_en))
    Path(f"merged/{lang}.txt").write_text("\n".join(merged_lang))
    print(f"{lang}: merged {len(merged_en)} lines")

