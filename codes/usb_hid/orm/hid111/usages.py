from universal_serial_bus.orm import ModelBuilder, OrmClassBase



def map_db_objects(db_url):
    engine, meta, tables, session = ModelBuilder.get_db_objects(db_url)
    script = ModelBuilder._gen_mapping_strings(db_url, print_out = False)
    exec(script)
    return engine, meta, tables, session



class AlphanumericDisplay(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class Button(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class Consumer(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class Digitizer(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_types, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_types = usage_types
        self.usage_id = usage_id
        self.page_id = page_id



class GameControl(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class GenericDesktop(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class GenericDeviceControl(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class KeyboardKeypad(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class Led(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class MedicalInstrument(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class Ordinal(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class SimulationControl(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class SportControl(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class Telephony(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id



class UsagePage(OrmClassBase):
    fields_sizes = []


    def __init__(self, page_name, description, code, page_id):
        self.page_name = page_name
        self.description = description
        self.code = code
        self.page_id = page_id



class VrControl(OrmClassBase):
    fields_sizes = []


    def __init__(self, usage_name, usage_type, usage_id, page_id):
        self.usage_name = usage_name
        self.usage_type = usage_type
        self.usage_id = usage_id
        self.page_id = page_id
