#!/bin/bash/python3

import os
import argparse

import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(prog="dfdiff", description="This program load two CSV files as string and use the Python Pandas library to identify the differences between two csv file. Written by Andy Chien andy_chien@hotmail.com -JAJA")
parser.add_argument('--files', metavar="FILE", nargs=2, required=True, help="The path to the left and right csv file")
parser.add_argument('--pkey', nargs='+', required=True, help="The list of primary keys to be used for joining the left and right table/csv")
parser.add_argument('--diffout', nargs=1, required=True, help="The output of the diff file")
parser.add_argument('--encoding', metavar="ENC", nargs=2, required=False, default=['latin_1','latin_1'], help="Encoding for the left and right csv")
parser.add_argument('--separators', metavar="SEP", nargs=2, required=False, default=[',',','], help="Separator for the left and right csv, use 't' for tab delimited file")

print(parser.parse_args())
