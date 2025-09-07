from glob import glob
from pathlib import Path
parallel_dirs = sorted(glob('*_parallel/'))

langs = ['de', 'fr', 'zh', 'pl', 'ru', 'tr','ar']
Path("merged").mkdir(exist_ok=True)

for lang in langs:
    merged_en, merged_lang = [], []
    for d in parallel_dirs:
        en_file = Path(d) / f"{lang}_en.txt"
        la_file = Path(d) / f"{lang}.txt"

        en_lines = en_file.read_text().strip().split('\n')
        la_lines = la_file.read_text().strip().split('\n')

        if len(en_lines) != len(la_lines):
            raise ValueError(f"Line mismatch in {d} for {lang}: {len(en_lines)} vs {len(la_lines)}")

        merged_en.extend(en_lines)
        merged_lang.extend(la_lines)

    Path(f"merged/{lang}_en.txt").write_text("\n".join(merged_en))
    Path(f"merged/{lang}.txt").write_text("\n".join(merged_lang))
    print(f"{lang}: merged {len(merged_en)} lines")

