import util
reload(util)
from util import * #for testing
updatepath('adviserinfo')

from formadv import *
#need categories

db = IapdDB()

DESCRIPTION_MAP = db.get_mapper('descriptions', 'id', 'desc')
DATEMAP = db.get_mapper('formadv', 'filingdate')
IDXFIELDS = ['crd', 'company', 'numberofclients',
             'numberofaccts', 'numberofemployees',
             'assetsundermgmt', 'aumdiff']
IDXFIELDSMAP = {
    'crd' : 'CRD#',
    'numberofaccts' : '# of Accounts',
    'numberofclients' : '# of Clients',
    'numberofemployees': '# of Employess',
    'assetsundermgmt': 'AUM',
    'aumdiff' : 'AUM Difference',
    'company' : 'Company Name'
        }

CATEGORIESMAP = {
    'pct_aum' : 'AUM% / Client Type',
    'client_types' : 'Types of Clients',
    'compensation': 'Compensation',
    'disclosures' : 'Reported Disclosures'
        }

class AdviserInfo(Project):
    Project.fldscnfg['idxtable'] = {'fields' : IDXFIELDS, 'fieldsmap' : IDXFIELDSMAP}
    CONTACTFIELDS = ['contactperson', 'phone', 'fax', 'url']
    DATAPATH = 'companylist.csv'
    
    def __init__(self, *args, **kwds):
        super(AdviserInfo, self).__init__(*args, **kwds)
        self.crdmap = self.df.get_mapper('crd', 'company')

    def conform(self, **kwds):
        df = super(AdviserInfo, self).conform(**kwds)
        return df.assign(AUM = self.df.assetsundermgmt.to_numeric().to_usd())

    @property
    def categories(self):
        __ = [
            ['pct_aum',(1, 13,)],
            ['client_types',(1, 13,)],
            ['compensation',(15, 19,)],
            ['disclosures' ,(2782, 2797,)],
                ]

        categories = OrderedDict()
        for k, v in __:
            _ = db.select('descriptions',
                fields = ['id'],
                subquery = "where id >= {} and id <= {}".format(*v)
                    ).id

            categories.update({
                k : {'name' : CATEGORIESMAP[k],
                     'items' : _.map(DESCRIPTION_MAP).tolist(),
                     'ids' : _.tolist()}})
        return categories

    @property
    def filters_dropdown(self):
        return {v['name'] : v['items'] for
            k, v in self.categories.items()}

#advinfo = AdviserInfo()