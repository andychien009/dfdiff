#!/usr/bin/bash

uv run ./main.py --files "../example/Cleared Building Permits since 2017.csv"  "../example/Cleared Building Permits since 2017-mod.csv" --pkey "_id" "PERMIT_NUM" --outcsv
