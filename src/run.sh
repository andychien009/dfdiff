#!/usr/bin/bash

uv run ./main.py --files "../data/Cleared Building Permits since 2017.csv"  "../data/Cleared Building Permits since 2017-mod.csv" --key "_id" "PERMIT_NUM" --outcsv
