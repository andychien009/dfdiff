#!/bin/bash/python3

import os
import argparse
from pathlib import Path
import sys

import pandas as pd
import numpy as np

from dfdiff.dfdiff import dfdiff

VER=0.8

parser = argparse.ArgumentParser(prog="dfdiff", description=f"This program load two CSV files as string into Python Pandas DataFrame to identify the differences. Version {VER}. This program is released under GPLv3 License. Written by Andy Chien andy_chien@hotmail.com -JAJA")
parser.add_argument('--files', metavar="FILE", nargs=2, required=True, help="The path to the left and right csv file")
parser.add_argument('--key', nargs='+', required=True, help="The list of join key to be used for joining the left and right table/csv. Composite key is supported, separated by space and enclosed by double quote if necessary.")
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
fdiff, cdiff, recdiff, dupkey = cmp.getDiffDfs()

fp = Path(uargs.files[1])
fstem = fp.stem
fabsp = fp.parent.resolve().absolute()

def outcsvinz(df, outfile):
    if df.shape[0] != 0:
        df.to_csv(outfile, index=False)

def pit(df, b, msg):
    if b:
        print(msg, file=sys.stderr)

fdiffnb = fdiff[fdiff['_merge']!='both'].shape[0]
pit(fdiff, fdiffnb != 0, 
     f"*** Feild Differences: {fdiffnb}")
pit(cdiff, cdiff.shape[0] != 0, f"*** Cell Data Differences: {cdiff.shape[0]}")
pit(recdiff, recdiff.shape[0] != 0, 
     f"*** Record Variances: {recdiff.shape[0]}")
pit(dupkey,  dupkey.shape[0] != 0, \
     f"*** Duplicated join key found, the diff result may not be\n"+
     f"    accurate for these duplicated join key, manual intervantion is needed\n" +
     f"    see outputs in '{fstem}-dupkey.csv' or \n" +
     f"    '{fstem}.xlsx' in sheet [dupkey] for more information.")

if uargs.outcsv:
    outcsvinz(fdiff, fabsp.joinpath(f"{fstem}-field.csv"))
    outcsvinz(cdiff, fabsp.joinpath(f"{fstem}-cell.csv"))
    outcsvinz(recdiff, fabsp.joinpath(f"{fstem}-rec.csv"))
    outcsvinz(dupkey, fabsp.joinpath(f"{fstem}-dupkey.csv"))

if uargs.outxlsx:
    with pd.ExcelWriter(fabsp.joinpath(fabsp,f"{fstem}.xlsx")) as O:
        fdiff.to_excel(O, sheet_name="fielddiff", index=False)
        cdiff.to_excel(O, sheet_name="celldiff", index=False)
        recdiff.to_excel(O, sheet_name="recdiff", index=False)
        dupkey.to_excel(O, sheet_name="dupkey", index=False)
