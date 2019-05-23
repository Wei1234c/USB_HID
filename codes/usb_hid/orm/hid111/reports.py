from universal_serial_bus.orm import OrmClassBase
from .items import *


bSIZE_SIZE = {0: 0, 1: 1, 2: 2, 3: 4}

USAGES_PAGES = {'00': 'Undefined',
                '01': 'Generic Desktop',
                '02': 'Simulation Controls',
                '03': 'VR Controls',
                '04': 'Sport Controls',
                '05': 'Game Controls',
                '06': 'Generic Device Controls',
                '07': 'Keyboard/Keypad',
                '08': 'LEDs',
                '09': 'Button',
                '0A': 'Ordinal',
                '0B': 'Telephony',
                '0C': 'Consumer',
                '0D': 'Digitizer',
                '0F': 'PID',
                '10': 'Unicode',
                '14': 'Alphanumeric Display',
                '40': 'Medical Instruments',
                '8C': 'Bar Code Scanner',
                '8D': 'Scale',
                '8E': 'Magnetic Stripe Reading (MSR) Devices',
                '8F': 'Reserved Point of Sales',
                '90': 'Camera Control',
                '91': 'Arcade'}

DATA_TYPE_BIT_MAP = {0: {0: 'Data', 1: 'Constant'},
                     1: {0: 'Array', 1: 'Variable'},
                     2: {0: 'Absolute', 1: 'Relative'},
                     3: {0: 'No Wrap', 1: 'Wrap'},
                     4: {0: 'Linear', 1: 'Non Linear'},
                     5: {0: 'Preferred State', 1: 'No Preferred'},
                     6: {0: 'No Null position', 1: 'Null state'},
                     7: {0: 'Non Volatile', 1: 'Volatile'},
                     8: {0: 'Bit Field', 1: 'Buffered Bytes'}}



class Parser:

    def __init__(self, usages_dictionary):
        self.idx_usages = get_idx_usage_names(usages_dictionary)
        self._init()


    def _init(self):
        self.usage_page_id = None


    def first_item_of_byte_array(self, byte_array):
        prefix = byte_array[0]
        bTag = OrmClassBase.int_to_hex(prefix >> 4).upper()
        bType = OrmClassBase.int_to_hex((prefix >> 2) & 0b00000011).upper()

        prefix_name = TAG_TYPE_PREFIXS[(bTag, bType)]

        data_size = bSIZE_SIZE[prefix & 0b00000011]
        data = array('B', byte_array[1:data_size + 1])
        data.reverse()
        data = OrmClassBase.byte_array_to_int(data) if len(data) > 0 else None

        page_name = self._get_usage_page_name(prefix_name, data)
        usage_name = self._get_usage_name(prefix_name, data)
        remained_byte_array = byte_array[1 + data_size:]
        return prefix_name, data_size, data, page_name, usage_name, remained_byte_array


    def _get_usage_name(self, prefix_name, data):
        if prefix_name == 'Usage':
            usage_id = OrmClassBase.int_to_hex(data).upper()
            usage_name = self.idx_usages.get((self.usage_page_id, usage_id), None)
            return usage_name


    def _get_bit_map_string(self, data):
        string = []
        for i in DATA_TYPE_BIT_MAP.keys():
            string.append(DATA_TYPE_BIT_MAP[i][(data >> i) & 1])
        return ' | '.join(string)


    def _get_collection_type(self, collection_id):
        return IDX_COLLECTIONS.get(OrmClassBase.int_to_hex(collection_id).upper())


    def _get_usage_page_name(self, prefix_name, data):
        if prefix_name == 'Usage Page':
            self.usage_page_id = OrmClassBase.int_to_hex(data).upper()
            return USAGES_PAGES.get(self.usage_page_id, 'Unknown')


    def parse(self, byte_array, print_byte_array = True):
        self._init()
        remained_byte_array = byte_array
        indent_spaces = 0

        if print_byte_array:
            print('\n###################################################')
            print(byte_array)
            print('###################################################')

        while len(remained_byte_array) > 0:
            prefix_name, data_size, data, page_name, usage_name, remained_byte_array = \
                self.first_item_of_byte_array(remained_byte_array)

            comment = None
            if prefix_name == 'Usage Page':
                comment = page_name
                print()
            if prefix_name == 'Usage':
                comment = usage_name
            if prefix_name in ['Input', 'Output', 'Feature']:
                comment = self._get_bit_map_string(data)
            if prefix_name == 'Collection':
                comment = self._get_collection_type(data)
            if prefix_name == 'End Collection':
                indent_spaces -= 2
                data = ''

            print(''.join([' '] * indent_spaces), prefix_name, data, '({})'.format(comment) if comment else '')

            if prefix_name == 'Collection':
                indent_spaces += 2

        print()



class ReportDescriptor:

    def __init__(self, items):
        self.from_items(items)


    def from_items(self, items):
        self.items = items


    def from_descriptor(self, descriptor):
        pass


    @property
    def byte_array(self):
        b_array = array('B', [])
        for item in self.items:
            b_array += item.byte_array
        return b_array
