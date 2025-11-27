#!/bin/bash/python3

import os
import argparse

import pandas as pd
import numpy as np

from dfdiff.dfdiff import dfdiff

VER=0.8

parser = argparse.ArgumentParser(prog="dfdiff", description=f"This program load two CSV files as string and use the Python Pandas library to identify the differences between two csv file. Version {VER}. Written by Andy Chien andy_chien@hotmail.com -JAJA")
parser.add_argument('--files', metavar="FILE", nargs=2, required=True, help="The path to the left and right csv file")
parser.add_argument('--pkey', nargs='+', required=True, help="The list of primary keys to be used for joining the left and right table/csv")
parser.add_argument('--outcsv', action='store_true', help="The output of the diff file", default=False)
parser.add_argument('--outxlsx', action='store_true', help="The output of the diff file", default=False)
parser.add_argument('--encoding', metavar="ENC", nargs=2, required=False, default=['latin_1','latin_1'], help="(optional) Encoding for the left and right csv")
parser.add_argument('--separators', metavar="SEP", nargs=2, required=False, default=[',',','], help="(optional) Separator for the left and right csv, use 't' for tab delimited file. Note that there may be differences reading in mixed tab separated file with regular csv file due to differences between pandas.read_table() and pandas.read_csv()")

uargs = parser.parse_args()

def loadfile(filenum):
    if uargs.separators == "t":
        with open(uargs.files[filenum], 'r', 
                  encoding=uargs.encoding[filenum]) as F:
            data = pd.read_table(F, dtype=str)
    else:
        with open(uargs.files[filenum], 'r', 
                  encoding=uargs.encoding[filenum]) as F:
            data = pd.read_csv(F, dtype=str, sep=uargs.separators[filenum])
    return data

left = loadfile(0)
right = loadfile(1)

cmp = dfdiff(left, right, uargs.pkey)
cdiff, recdiff = cmp.getDiffDfs()

if uargs.outcsv:
    cdiff.to_csv("diff-cell.csv", index=False)
    recdiff.to_csv("diff-rec.csv", index=False)

if uargs.outxlsx:
    with pd.ExcelWriter("diff.xlsx") as O:
        cdiff.to_excel(O, sheet_name="celldiff", index=False)
        recdiff.to_excel(O, sheet_name="recdiff", index=False)
