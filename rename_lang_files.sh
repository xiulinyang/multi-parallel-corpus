#!/bin/bash
# Rename TED2020 bilingual files into consistent format
CORPUS=$1
DIR=$2
ZHN=$3
cd $DIR
rm *.xml
for lang in pl fr tr ru $ZHN; do
    echo $lang
    
    if [ -f "$CORPUS.en-$lang.en" ]; then
        mv "$CORPUS.en-$lang.en" "${lang}_en.txt"
    fi

    if [ -f "$CORPUS.en-$lang.$lang" ]; then
        mv "$CORPUS.en-$lang.$lang" "${lang}.txt"
    fi
done

for lang in ar de; do
    echo $lang

    if [ -f "$CORPUS.$lang-en.en" ]; then
        mv "$CORPUS.$lang-en.en" "${lang}_en.txt"
    fi

    if [ -f "$CORPUS.$lang-en.$lang" ]; then
        mv "$CORPUS.$lang-en.$lang" "${lang}.txt"
    fi
done
