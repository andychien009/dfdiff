import pandas as pd
import numpy as np

class dfdiff():
    def __init__(self, l, r, key):
        self.key = key
        self.l = l
        self.r = r
        self.lcol = l.columns.to_list()
        self.rcol = r.columns.to_list()
        self.inlnotr = [x for x in self.lcol if x not in self.rcol ]
        self.inrnotl = [x for x in self.rcol if x not in self.lcol ]
        self.scol = [x for x in self.lcol if x in self.rcol and x not in self.key ]
        self.l[self.l.columns] = self._procCols(self.l)
        self.r[self.r.columns] = self._procCols(self.r)
        self.m = self.l.merge(self.r, how='outer', on=self.key, 
                         suffixes=('_l','_r'), indicator=True)
        self.diffdf = None

        # do pkey uniqueness test
        if self.m.shape[0] != self.l.shape[0] or self.m.shape[0] != self.r.shape[0]:
            print("*** duplicated records are created because join key is not unique")

    def _procCols(self, df):
        ret = df.copy()
        ret[ret.columns] = ret.apply(lambda c: c.fillna(""))
        ret[ret.columns] = ret.apply(lambda c: c.str.strip())
        return ret

    def printDiff(self):
        if self.diffdf is None:
            self._getDiffDf()
        for c in self.scol:
            coldiff = self.diffdf[self.diffdf['fname']==c]
            if coldiff.shape[0] != 0:
                print(f"Difference found in '{c}' Field")
                print(f"{coldiff}\n")

    def getFieldDiffList(self):
        if self.diffdf is None:
            self._getDiffDf()
        return self.diffdf['fname'].unique().tolist()

    def getDiffDf(self):
        if self.diffdf is None:
            self._getDiffDf()
            return self.diffdf
        else:
            return self.diffdf

    def _getDiffDf(self):
        diffdf = None
        for c in self.scol:
            cols = [f"{c}_l", f"{c}_r"]
            diffdata = ['fname','lval','rval']
            coldiffdf = self.m[self.m[cols[0]] != self.m[cols[1]]]
            if coldiffdf.shape[0] != 0:
                mapper = dict(zip(cols,['lval','rval']))
                coldiffdf = coldiffdf.rename(columns=mapper)
                coldiffdf['fname'] = c
                coldiff = coldiffdf[self.key+diffdata].copy()
                if diffdf is None:
                    diffdf = coldiff
                else:
                    diffdf = pd.concat([diffdf, coldiff])

        if diffdf is None:
            self.diffdf = pd.DataFrame(
                    columns=[self.key+diffdata],
                    dtype=str)
        else:
            self.diffdf = diffdf.reset_index()

    def __repr__(self):
        return f"""\
Field in l not r: {self.inlnotr}
Field in r not l: {self.inrnotl}
Field shared between dataframe: {self.scol}
Number of field with differences is observed: {self.getFieldDiffList()}
"""
