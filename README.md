# multi-parallel-corpus
The repository for building multilingual parallel corpus.
## Step 1: Download the datasets in the moses format and rename the files.
Moses format refers to one source language txt file and one target language file which each line being the translation of the other.
```bash
# download the english centric parallel corpora
bash download_data.sh Corpus_Name Target_Dir ZH_lang_code
# rename the corpora to lang.txt and en_lang.txt.
bash rename_lang_files.sh Corpus_Name  Target_Dir ZH_lang_code
```

## Step 2: find parallel corpus for each corpus separately
```bash 
python find_parallel.py -s source_dir -t target_dir
```
## Step 3: merge and clean the data

```bash
python merge_files.py -s source_dir -t target_dir
python clean_and_compile_data.py 
```

## Step 4: further cleaning caught by manual assessment and find the overlap shared by all languages (again)
```bash
python further_clean.py 
python find_parallel.py -s source_dir -t target_dir
```

