import math
from array import array

from orm.tools import AttrDict


SIZE_bSIZE = {0: 0, 1: 1, 2: 2, 4: 3}

COLLECTION_TYPES = AttrDict({'Physical'      : '00',
                             'Application'   : '01',
                             'Logical'       : '02',
                             'Report'        : '03',
                             'Named_Array'   : '04',
                             'Usage_Switch'  : '05',
                             'Usage_Modifier': '06'})

IDX_COLLECTIONS = {v: k for k, v in COLLECTION_TYPES.items()}

PREFIXS = AttrDict({'Input'             : {'id': 1, 'item_name': 'Input', 'bType': '00', 'bTag': '08'},
                    'Output'            : {'id': 2, 'item_name': 'Output', 'bType': '00', 'bTag': '09'},
                    'Feature'           : {'id': 3, 'item_name': 'Feature', 'bType': '00', 'bTag': '0B'},
                    'Collection'        : {'id'       : 4,
                                           'item_name': 'Collection',
                                           'bType'    : '00',
                                           'bTag'     : '0A'},
                    'End_Collection'    : {'id'       : 5,
                                           'item_name': 'End Collection',
                                           'bType'    : '00',
                                           'bTag'     : '0C'},
                    'Usage_Page'        : {'id'       : 6,
                                           'item_name': 'Usage Page',
                                           'bType'    : '01',
                                           'bTag'     : '00'},
                    'Logical_Minimum'   : {'id'       : 7,
                                           'item_name': 'Logical Minimum',
                                           'bType'    : '01',
                                           'bTag'     : '01'},
                    'Logical_Maximum'   : {'id'       : 8,
                                           'item_name': 'Logical Maximum',
                                           'bType'    : '01',
                                           'bTag'     : '02'},
                    'Physical_Minimum'  : {'id'       : 9,
                                           'item_name': 'Physical Minimum',
                                           'bType'    : '01',
                                           'bTag'     : '03'},
                    'Physical_Maximum'  : {'id'       : 10,
                                           'item_name': 'Physical Maximum',
                                           'bType'    : '01',
                                           'bTag'     : '04'},
                    'Unit_Exponent'     : {'id'       : 11,
                                           'item_name': 'Unit Exponent',
                                           'bType'    : '01',
                                           'bTag'     : '05'},
                    'Unit'              : {'id': 12, 'item_name': 'Unit', 'bType': '01', 'bTag': '06'},
                    'Report_Size'       : {'id'       : 13,
                                           'item_name': 'Report Size',
                                           'bType'    : '01',
                                           'bTag'     : '07'},
                    'Report_ID'         : {'id'       : 14,
                                           'item_name': 'Report ID',
                                           'bType'    : '01',
                                           'bTag'     : '08'},
                    'Report_Count'      : {'id'       : 15,
                                           'item_name': 'Report Count',
                                           'bType'    : '01',
                                           'bTag'     : '09'},
                    'Push'              : {'id': 16, 'item_name': 'Push', 'bType': '01', 'bTag': '0A'},
                    'Pop'               : {'id': 17, 'item_name': 'Pop', 'bType': '01', 'bTag': '0B'},
                    'Usage'             : {'id': 18, 'item_name': 'Usage', 'bType': '02', 'bTag': '00'},
                    'Usage_Minimum'     : {'id'       : 19,
                                           'item_name': 'Usage Minimum',
                                           'bType'    : '02',
                                           'bTag'     : '01'},
                    'Usage_Maximum'     : {'id'       : 20,
                                           'item_name': 'Usage Maximum',
                                           'bType'    : '02',
                                           'bTag'     : '02'},
                    'Designator_Index'  : {'id'       : 21,
                                           'item_name': 'Designator Index',
                                           'bType'    : '02',
                                           'bTag'     : '03'},
                    'Designator_Minimum': {'id'       : 22,
                                           'item_name': 'Designator Minimum',
                                           'bType'    : '02',
                                           'bTag'     : '04'},
                    'Designator_Maximum': {'id'       : 23,
                                           'item_name': 'Designator Maximum',
                                           'bType'    : '02',
                                           'bTag'     : '05'},
                    'String_Index'      : {'id'       : 24,
                                           'item_name': 'String Index',
                                           'bType'    : '02',
                                           'bTag'     : '07'},
                    'String_Minimum'    : {'id'       : 25,
                                           'item_name': 'String Minimum',
                                           'bType'    : '02',
                                           'bTag'     : '08'},
                    'String_Maximum'    : {'id'       : 26,
                                           'item_name': 'String Maximum',
                                           'bType'    : '02',
                                           'bTag'     : '09'},
                    'Delimiter'         : {'id'       : 27,
                                           'item_name': 'Delimiter',
                                           'bType'    : '02',
                                           'bTag'     : '0A'}})

TAG_TYPE_PREFIXS = {(v['bTag'], v['bType']): k for k, v in PREFIXS.items()}



def get_usages_dictionary(fn = 'usb_hid_report_item_usages.json'):
    return AttrDict.load(fn)



def get_idx_usage_names(usages_dictionary):
    idx_usages = {}
    for page, usages in usages_dictionary.items():
        if page != 'usage_pages':
            for usage, attrs in usages.items():
                idx_usages[(attrs['page_id'], attrs['usage_id'])] = usage

    return idx_usages



class Item:

    def __init__(self, prefix, value = None):
        self.prefix = prefix
        self.value = self._convert_value(value)


    @classmethod
    def _convert_value(cls, value):
        if value is not None:
            return value if isinstance(value, int) else int(value, 16)


    @property
    def bTag(self):
        return int(self.prefix.bTag, 16)


    @property
    def bType(self):
        return int(self.prefix.bType, 16)


    @property
    def bSize(self):
        length = 0 if self.value is None else max(math.ceil(math.log2(self.value + 1) / 8), 1)
        return SIZE_bSIZE[length]


    @property
    def tag_type(self):
        _tag = (self.bTag & 0b1111) << 2
        _type = self.bType & 0b11
        return (_tag | _type) << 2


    @property
    def tag_type_size(self):
        return self.tag_type | self.bSize


    @property
    def byte_array(self):
        b_array = array('B', [self.tag_type_size] if self.value is None else [self.value, self.tag_type_size])
        b_array.reverse()
        return b_array
