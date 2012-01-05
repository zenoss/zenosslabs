#!/bin/bash


DBDIR="./data_bags/"

for databag in `ls -1 $DBDIR`;
do
    echo "== uploading data for $databag"
    for ditem in `ls -1 $DBDIR$databag/`; 
    do
        echo "   uploading $ditem"
        knife data bag from file $databag $DBDIR$databag/$ditem
    done
done
