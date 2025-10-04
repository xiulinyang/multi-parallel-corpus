#!/bin/bash

# This script downloads 3 languages from OPUS using opus api

CORPUS=$1
TDIR=$2
RELEASE=$3
ZHCODE=$4

mkdir $TDIR
for lang in ar $ZHCODE; do
    echo "Downloading $CORPUS en-$lang into $TDIR"
    yes | opus_get -s en -t $lang -d $CORPUS -p moses -dl $TDIR -r $RELEASE
done

cd $TDIR
yes | unzip '*.zip'
rm -rf *.zip
cd ..

