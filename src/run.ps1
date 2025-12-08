#!/usr/bin/bash

python.exe .\dfdiff.py --files "../data/Cleared Building Permits since 2017.csv"  "../data/Cleared Building Permits since 2017-mod.csv" --key "_id" "PERMIT_NUM" --outcsv --outxlsx
