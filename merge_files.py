from glob import glob
from pathlib import Path
parallel_dirs = sorted(glob('*_parallel/'))

langs = ['ar','de', 'fr', 'zh', 'pl', 'ru', 'tr']
Path("merged").mkdir(exist_ok=True)

for lang in langs:
    with open(f'merged/{lang}_en.txt', 'w') as en, open(f'merged/{lang}.txt', 'w') as la:
        merged_en = [Path(f'{x}/{lang}_en.txt').read_text().strip() for x in parallel_dirs]
        merged_lang = [Path(f'{x}/{lang}.txt').read_text().strip() for x in parallel_dirs]
        merged_en_check = [len(x.split('\n')) for x in merged_en]
        merged_lang_check = [len(x.split('\n')) for x in merged_lang]
        print(merged_en_check, merged_lang_check)
        assert merged_en_check == merged_lang_check
        en.write('\n'.join(merged_en))
        la.write('\n'.join(merged_lang))

