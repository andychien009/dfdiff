#!/usr/bin/bash

python.exe .\dfdiff.py --files "../example/Cleared Building Permits since 2017.csv"  "../example/Cleared Building Permits since 2017.csv" --pkey "_id" "PERMIT_NUM" --outcsv --outxlsx
