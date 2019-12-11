import json

from .items import *


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

    def __init__(self):
        from .usages.dictionary import USAGES

        self.idx_usages = get_idx_usage_names(USAGES)
        self._init()


    def _init(self):
        self.usage_page_id = None


    def first_item_of_byte_array(self, byte_array):
        item = Item.from_byte_array(byte_array)
        remained_byte_array = byte_array[1 + item.value_size:]
        return item, remained_byte_array


    def parse(self, byte_array, print_out = False):
        self._init()
        items = []
        lines = []
        remained_byte_array = byte_array
        indent_spaces = 0
        indent_spaces_step = 2

        lines.append('')
        lines.append('###################################################')
        lines.append(str(byte_array))
        lines.append('###################################################')

        while len(remained_byte_array) > 0:
            item, remained_byte_array = self.first_item_of_byte_array(remained_byte_array)
            prefix_type = item.prefix_type_name

            comment = None
            if prefix_type == 'Usage_Page':
                comment = self._get_usage_page_name(prefix_type, item.value)
                lines.append('')
            if prefix_type == 'Usage':
                comment = self._get_usage_name(prefix_type, item.value)
            if prefix_type in ['Input', 'Output', 'Feature']:
                comment = self._get_bit_map_string(int.from_bytes(item.value.tobytes(), 'little'))
            if prefix_type == 'Collection':
                comment = IDX_COLLECTIONS.get(item.value.tobytes().hex().upper())
            if prefix_type == 'End_Collection':
                indent_spaces -= indent_spaces_step
                # data = ''
            signed = True if prefix_type in ('Logical_Minimum', 'Logical_Maximum') else False

            lines.append('{} {} {} {}'.format(''.join([' '] * indent_spaces),
                                              prefix_type,
                                              '' if item.value_size == 0 else
                                              int.from_bytes(item.value.tobytes(), 'little', signed = signed),
                                              '({})'.format(comment) if comment else ''))
            if prefix_type == 'Collection':
                indent_spaces += indent_spaces_step

            prefix = AttrDict(PREFIX_TYPES.get(prefix_type))
            items.append(Item(prefix, item.value))

        lines.append('')
        lines = '\n'.join(lines)

        if print_out:
            print(lines)

        return lines, ReportDescriptor(items)


    def _get_usage_page_name(self, prefix_type, data):
        self.usage_page_id = data.tobytes().hex().upper()
        return USAGES_PAGES.get(self.usage_page_id, 'Unknown')


    def _get_usage_name(self, prefix_type, data):
        usage_id = data.tobytes().hex().upper()
        usage_name = self.idx_usages.get((self.usage_page_id, usage_id), None)
        return usage_name


    def _get_bit_map_string(self, data):
        string = []
        for i in DATA_TYPE_BIT_MAP.keys():
            string.append(DATA_TYPE_BIT_MAP[i][(data >> i) & 1])
        return ' | '.join(string)



class ReportDescriptor:

    def __init__(self, items):
        self.items = items


    @classmethod
    def from_descriptor(cls, descriptor):
        parser = Parser()
        _, obj = parser.parse(descriptor)
        return obj


    @property
    def byte_array(self):
        b_array = array('B', [])
        for item in self.items:
            b_array += item.byte_array
        return b_array


    def parse(self, print_out = False, save_as_file = False, file_name = 'HID_report_descriptor.txt'):
        parser = Parser()
        lines, _ = parser.parse(self.byte_array, print_out = print_out)

        if save_as_file:
            with open(file_name, 'wt') as f:
                f.writelines(lines)

        return lines


    def dump(self, file_name = 'HID_report_descriptor.json'):
        with open(file_name, 'wt') as f:
            json.dump(self.byte_array.tolist(), f)


    @classmethod
    def load(cls, file_name = 'report_descriptor.json'):
        with open(file_name, 'rt') as f:
            return cls.from_descriptor(array('B', json.load(f)))
