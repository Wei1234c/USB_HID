from universal_serial_bus.orm import ModelBuilder, OrmClassBase



def map_db_objects(db_url):
    engine, meta, tables, session = ModelBuilder.get_db_objects(db_url)
    script = ModelBuilder._gen_mapping_strings(db_url, print_out = False)
    exec(script)
    return engine, meta, tables, session



class HidDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('bcdHID', 2), ('bCountryCode', 1), ('bNumDescriptors', 1),
                    ('bReportDescriptorType', 1), ('wReportDescriptorLength', 2), ]


    def __init__(self, bLength, bDescriptorType, bcdHID, bCountryCode, bNumDescriptors, bReportDescriptorType,
                 wReportDescriptorLength, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bcdHID = bcdHID
        self.bCountryCode = bCountryCode
        self.bNumDescriptors = bNumDescriptors
        self.bReportDescriptorType = bReportDescriptorType
        self.wReportDescriptorLength = wReportDescriptorLength
