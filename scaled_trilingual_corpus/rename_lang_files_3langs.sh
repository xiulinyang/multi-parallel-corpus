#!/bin/bash

CORPUS=$1
DIR=$2
ZHN=$3
cd $DIR
rm *.xml
  
if [ -f "$CORPUS.en-$ZHN.en" ]; then
        mv "$CORPUS.en-$ZHN.en" "${ZHN}_en.txt"
fi

if [ -f "$CORPUS.en-$ZHN.$ZHN" ]; then
        mv "$CORPUS.en-$ZHN.$ZHN" "${ZHN}.txt"
fi



if [ -f "$CORPUS.ar-en.en" ]; then
        mv "$CORPUS.ar-en.en" "ar_en.txt"
fi

if [ -f "$CORPUS.ar-en.ar" ]; then
        mv "$CORPUS.ar-en.ar" "ar.txt"
fi

