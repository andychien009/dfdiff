#!/bin/bash/python3

import os
import argparse
from pathlib import Path

import pandas as pd
import numpy as np

from dfdiff.dfdiff import dfdiff

VER=0.8

parser = argparse.ArgumentParser(prog="dfdiff", description=f"This program load two CSV files as string into Python Pandas DataFrame to identify the differences. Version {VER}. Written by Andy Chien andy_chien@hotmail.com -JAJA")
parser.add_argument('--files', metavar="FILE", nargs=2, required=True, help="The path to the left and right csv file")
parser.add_argument('--pkey', nargs='+', required=True, help="The list of primary keys to be used for joining the left and right table/csv")
parser.add_argument('--outcsv', action='store_true', help="The output of the diff file using CSV file. This output method maybe preferred if the XLSX output experiences performance issues due to the size of the output data.", default=False)
parser.add_argument('--outxlsx', action='store_true', help="The output of the diff file. This output method is good for Excel-ready analysis, however it may experience performance issue as output size grow. Try --outcsv if the program takes too long to output.", default=False)
parser.add_argument('--encoding', metavar="ENC", nargs=2, required=False, default=['latin_1','latin_1'], help="(optional) Encoding for the left and right csv")
parser.add_argument('--separators', metavar="SEP", nargs=2, required=False, default=[',',','], help="(optional) Separator for the left and right csv, use 't' for tab delimited file. Note that there may be differences reading in mixed tab separated file with regular csv file due to differences between pandas.read_table() and pandas.read_csv()")
parser.add_argument('--version', action='version', version=f"%(prog)s {VER}")

uargs = parser.parse_args()

def loadfile(filenum):
    if uargs.separators[filenum] == "t":
        with open(uargs.files[filenum], 'r', 
                  encoding=uargs.encoding[filenum]) as F:
            data = pd.read_table(F, dtype=str, low_memory=False)
    else:
        with open(uargs.files[filenum], 'r', 
                  encoding=uargs.encoding[filenum]) as F:
            data = pd.read_csv(F, dtype=str, sep=uargs.separators[filenum],
                  low_memory=False)
    return data

left = loadfile(0)
right = loadfile(1)

cmp = dfdiff(left, right, uargs.pkey)
print(f"{cmp}")
cdiff, recdiff = cmp.getDiffDfs()

fp = Path(uargs.files[1])
fstem = fp.stem
fabsp = fp.parent.resolve().absolute()

if uargs.outcsv:
    cdiff.to_csv(fabsp.joinpath(f"{fstem}-cell.csv"), index=False)
    recdiff.to_csv(fabsp.joinpath(f"{fstem}-rec.csv"), index=False)

if uargs.outxlsx:
    with pd.ExcelWriter(fabsp.joinpath(fabsp,f"{fstem}.xlsx")) as O:
        cdiff.to_excel(O, sheet_name="celldiff", index=False)
        recdiff.to_excel(O, sheet_name="recdiff", index=False)
