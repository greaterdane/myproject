import os
import sys
import pandas as pd
from stagelib.generic import mergedicts

def updatepath(projectname):
    thisdir = os.path.dirname(os.path.abspath(__name__))
    basedir = os.path.dirname(thisdir)
    sys.path.append(os.path.join(basedir, projectname))

class Project(object):
    fldscnfg = {'idxtable' : {'fields' : [], 'fieldsmap' : {}}}
    funcmap = [('df', 'conform',), ('ajax', 'to_ajax',)]

    def __init__(self, tabledata = None, *args, **kwds):
        if not tabledata:
            tabledata = pd.read_csv(self.DATAPATH, **kwds)
        self.df = tabledata
        self.load()

    def load(self):
        for key in self.fldscnfg:
            for k, v in self.funcmap:
                setattr(self, "{}_{}".format(key, k),
                    getattr(self, v)(tbltype = key))

    def conform(self, tbltype = 'idxtable'):
        __ = self.fldscnfg[tbltype]
        return self.df.fillna('n/a').ix[:,
            __['fields']].rename(columns = __['fieldsmap'])

    def to_ajax(self, tbltype = 'idxtable', dtconfig = {}):
        __ = {'data' : getattr(self, "{}_df".format(tbltype)).values.tolist()}
        return mergedicts(__, dtconfig)
