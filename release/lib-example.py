#!/usr/bin/python

import pandas as pd

from dfdiff.dfdiff import dfdiff

F1="left.csv"
F2="right.csv"

with open(F1, 'r', encoding='latin_1') as F:
    left = pd.read_csv(F, dtype=str, low_memory=False)

with open(F2, 'r', encoding='latin_1') as F:
    right = pd.read_csv(F, dtype=str, low_memory=False)

# suppose we want to pad 0 in the id before we start comparison
left['id'] = left['id'].str.pad("0", side="left", fillchar="0")

cmp = dfdiff(left, right, ['id','compkey'])
fdiff, cdiff, recdiff, dupkey = cmp.getDiffDfs()

print(fdiff.head())
print(cdiff.head())
print(recdiff.head())
print(dupkey.head())
