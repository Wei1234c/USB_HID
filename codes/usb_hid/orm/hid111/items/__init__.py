import math
from array import array

from orm.tools import AttrDict


SIZE_bSIZE = {0: 0, 1: 1, 2: 2, 4: 3}
bSIZE_SIZE = {v: k for k, v in SIZE_bSIZE.items()}

COLLECTION_TYPES = AttrDict({'Physical'      : '00',
                             'Application'   : '01',
                             'Logical'       : '02',
                             'Report'        : '03',
                             'Named_Array'   : '04',
                             'Usage_Switch'  : '05',
                             'Usage_Modifier': '06'})

IDX_COLLECTIONS = {v: k for k, v in COLLECTION_TYPES.items()}

PREFIX_TYPES = AttrDict({'Input'             : {'id': 1, 'item_name': 'Input', 'bType': '00', 'bTag': '08'},
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

TAG_TYPE_PREFIX_TYPES = {(v['bTag'], v['bType']): k for k, v in PREFIX_TYPES.items()}



def get_usages_dictionary(file_name = 'usb_hid_report_item_usages.json'):
    return AttrDict.load(file_name)



def get_idx_usage_names(usages_dictionary):
    idx_usages = {}
    for page, usages in usages_dictionary.items():
        if page != 'usage_pages':
            for usage, attrs in usages.items():
                idx_usages[(attrs['page_id'], attrs['usage_id'])] = usage

    return idx_usages



class Item:

    def __init__(self, prefix_type, value = array('B', [])):
        """
        :param prefix_type: Prefix object
        :param value: little endian byte_array or hex
        """
        self.bTag = int(prefix_type['bTag'], 16)
        self.bType = int(prefix_type['bType'], 16)
        self.value = self._convert_value(value)


    @classmethod
    def _convert_value(cls, value):
        if isinstance(value, int):
            size = max(math.ceil(math.log2(value + 1) / 8), 1)
            value = array('B', value.to_bytes(size, 'little'))
        if isinstance(value, bytes):
            value = array('B', value)
        if isinstance(value, str):
            value = array('B', bytes.fromhex(value))
        return value


    @classmethod
    def from_byte_array(cls, byte_array):
        """
        :param byte_array: little endian byte_array
        :return:
        """
        first_byte = byte_array[0]

        bTag = hex((first_byte >> 4) & 0b00001111)
        bType = hex((first_byte >> 2) & 0b00000011)
        value_size = bSIZE_SIZE[first_byte & 0b00000011]

        prefix_type = {'bTag': bTag, 'bType': bType}
        value = byte_array[1:1 + value_size]

        return cls(prefix_type, value)


    @property
    def value_size(self):
        return len(self.value)


    @property
    def bSize(self):
        return SIZE_bSIZE[self.value_size]


    @property
    def prefix(self):
        _tag = (self.bTag & 0b1111) << 4
        _type = (self.bType & 0b11) << 2
        return _tag | _type | self.bSize


    @property
    def byte_array(self):
        return array('B', [self.prefix]) + self.value


    @property
    def prefix_type_name(self):
        return TAG_TYPE_PREFIX_TYPES[(self.bTag.to_bytes(1, 'little').hex().upper(),
                                      self.bType.to_bytes(1, 'little').hex().upper())]


    @property
    def prefix_type(self):
        return PREFIX_TYPES.get(self.prefix_type_name)
