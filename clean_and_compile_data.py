'''
This script is used to
(1) clean the data using fasttext to remove English text from non-English corpus;
(2) build tsv en-lang pairs with corresponding corpus for further manual check
'''
import fasttext
from huggingface_hub import hf_hub_download
from glob import glob
from pathlib import Path
import csv
import re, unicodedata
from tqdm import tqdm
model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")
model = fasttext.load_model(model_path)



EXPECTED_SCRIPT = {
    "zh": "HAN",
    "ar": "ARABIC",
    "ru": "CYRILLIC",
    "ko": "HANGUL"
}

def _script_name(ch: str) -> str:
    try:
        name = unicodedata.name(ch)
    except ValueError:
        return "OTHER"
    if "CJK UNIFIED IDEOGRAPH" in name:
        return "HAN"
    for tag in ("LATIN", "ARABIC", "CYRILLIC", "HANGUL"):
        if tag in name:
            return tag
    return "OTHER"

def _script_ratio(text: str, script: str) -> float:
    if not text:
        return 0.0
    wanted = 0
    total_letters = 0
    for ch in text:
        if ch.isalpha():
            total_letters += 1
            if _script_name(ch) == script:
                wanted += 1
    return (wanted / total_letters) if total_letters else 0.0

def _alpha_ratio(text: str) -> float:
    letters = sum(ch.isalpha() for ch in text)
    return letters / max(1, len(text))

def _punct_digit_ratio(text: str) -> float:
    bad = sum(ch.isdigit() or unicodedata.category(ch).startswith('P') for ch in text)
    return bad / max(1, len(text))

_WORD = re.compile(r"[^\W_]+", flags=re.UNICODE)  # unicode word chars, no underscore

def _tok(s: str):
    s = unicodedata.normalize("NFKC", s).casefold()
    return _WORD.findall(s)

def ngram_jaccard(a: str, b: str, n: int = 1):
    A, B = _tok(a), _tok(b)
    def ngrams(seq, n):
        return {" ".join(seq[i:i+n]) for i in range(len(seq)-n+1)}
    NA, NB = ngrams(A, n), ngrams(B, n)
    if not NA and not NB:
        return len(A)
    return len(A)-len(NA & NB)

def clean_en(
    languages,
    illegal_log_name = 'filtered_out_data.tsv',
    merged_dir="merged_parallel",
    min_tgt_len=3,
    max_punct_digit_ratio=0.5,
    min_script_ratio=0.5,
    ngram_overlap=2
):
    with (open(illegal_log_name, "a", encoding="utf-8") as illegal_log):
        removed = []
        chinese_pair = {}
        for lang in tqdm(languages):
            en_path = Path(merged_dir) / f"{lang}_en.txt"
            lg_path = Path(merged_dir) / f"{lang}.txt"

            en_text = en_path.read_text(encoding="utf-8").strip().split("\n")
            lg_text = lg_path.read_text(encoding="utf-8").strip().split("\n")
            assert len(en_text) == len(lg_text), f"Length mismatch for {lang}"

            labels, _ = model.predict(lg_text)
            expected = EXPECTED_SCRIPT.get(lang, "LATIN")

            for en_sent, lg_sent, lbl in tqdm(zip(en_text, lg_text, labels)):
                en_s = en_sent.strip()
                lg_s = lg_sent.strip()
                if len(lg_s) <= min_tgt_len:
                    illegal_log.write(f'{lang}\t{en_sent}\t{lg_sent}\ttext too short.\t{len(lg_s)}\n')
                    removed.append(en_sent)

                # overlap with english
                if ngram_jaccard(en_s, lg_s) < ngram_overlap:
                    if lang =='zh': #special treatments of chinese
                        letters = [_script_name(c) for c in lg_s]
                        if 'LATIN' in letters:
                            letter_id = letters.index('LATIN')
                        else:
                            letter_id = len(letters)
                        if '{' in lg_s:
                            punc_id = lg_s.index('{')
                        else:
                            punc_id = len(lg_s)
                        new_text = lg_sent[:min(letter_id, punc_id)]
                        if ngram_jaccard(en_s, new_text) < ngram_overlap or _script_ratio(new_text, expected) < min_script_ratio or len(new_text)<4:
                            illegal_log.write(f'{lang}\t{en_sent}\t{lg_sent}\ttoo much overlap.\t_\n')
                            removed.append(en_sent)
                        else:
                            chinese_pair[en_sent] = new_text.strip()
                            continue
                    else:
                        illegal_log.write(f'{lang}\t{en_sent}\t{lg_sent}\ttoo much overlap.\t_\n')
                        removed.append(en_sent)

                if lbl[0].startswith("__label__en"):
                    if lang=='zh' and len(lg_sent)>2:
                        if _script_name(lg_sent[-2]) =='HAN':
                            chinese_pair[en_sent] = lg_sent.strip()
                            continue
                    illegal_log.write(f'{lang}\t{en_sent}\t{lg_sent}\ttext is English.\t{lbl[0]}\n')
                    removed.append(en_sent)
                # percentage of punctuations
                pr = _punct_digit_ratio(lg_s)
                if pr > max_punct_digit_ratio:
                    illegal_log.write(f'{lang}\t{en_sent}\t{lg_sent}\ttoo many punctuataion.\t{pr}\n')
                    removed.append(en_sent)


                # percentage of letters for non latin languages.
                if expected != "LATIN":
                    if _script_ratio(lg_s, expected) < min_script_ratio:
                        illegal_log.write(f'{lang}\t{en_sent}\t{lg_sent}\ttoo many letters.\t_\n')
                        removed.append(en_sent)

    #deduplicate
    return set(removed), chinese_pair


def build_en_source_dict(lang, multilingual_parallel_dirs, chinese_pair):
    lang_source_dict = {}
    for m_dir in multilingual_parallel_dirs:
        en_data = Path(f'{m_dir}/{lang}_en.txt').read_text().strip().split('\n')
        m_data = Path(f'{m_dir}/{lang}.txt').read_text().strip().split('\n')
        assert len(en_data) == len(m_data)
        source_name = m_dir.split('_')[0]
        for sent_en, sent_l in zip(en_data, m_data):
            if lang=='zh':
                if sent_en in chinese_pair:
                    sent_l = chinese_pair[sent_en]
            if sent_en not in lang_source_dict:
                lang_source_dict[sent_en] = {'source':[source_name],
                                          'trans': [sent_l]}
            else:
                lang_source_dict[sent_en]['source'].append(source_name)
                lang_source_dict[sent_en]['trans'].append(sent_l)
    return lang_source_dict

def build_lang_pair(en_text_list, languages, multilingual_parallel_dirs, chinese_pair, out_dir='cleaned_parallel'):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for lang in tqdm(languages):
        meta = build_en_source_dict(lang, multilingual_parallel_dirs, chinese_pair)
        out_path = Path(f'{out_dir}/en_{lang}.tsv')
        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(["en", "trans", "source"])

            for en_sent in en_text_list:
                if en_sent not in meta:
                    continue
                trans = meta[en_sent]["trans"][0]
                source = "&".join(meta[en_sent]["source"])
                writer.writerow([en_sent, trans, source])


if __name__ =='__main__':
    parallel_dirs = sorted(glob('*_parallel/'))
    parallel_dirs = [x for x in parallel_dirs if 'merge' not in x]
    langs = ['de', 'fr', 'zh', 'pl', 'ru', 'tr', 'ar','fi', 'ko']
    removed_en_list, chinese_pairs = clean_en(langs)
    en_zh_path = Path("merged_parallel/zh_en.txt")
    en_text_all = en_zh_path.read_text(encoding="utf-8").strip().split("\n")
    en_list = [x for x in en_text_all if x not in removed_en_list]
    print(len(en_list))
    print(sum([len(x.split()) for x in en_list]))
    build_lang_pair(en_list, langs, parallel_dirs, chinese_pairs)
