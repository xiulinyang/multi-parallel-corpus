#!/bin/bash

# This script downloads 10 languages from OPUS using opus api

CORPUS=$1
TDIR=$2
ZHCODE=$3 # the chinese lang code. It might differ in different corpora

mkdir $TDIR
for lang in ar de fr ru tr pl $ZHCODE; do
    echo "Downloading $CORPUS en-$lang into $TDIR"
    yes | opus_get -s en -t $lang -d $CORPUS -p moses -dl $TDIR -r latest
done

cd $TDIR
yes | unzip '*.zip'
rm -rf *.zip
cd ..

