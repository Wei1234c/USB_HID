from universal_serial_bus.orm import ModelBuilder, OrmClassBase



def map_db_objects(db_url):
    engine, meta, tables, session = ModelBuilder.get_db_objects(db_url)
    script = ModelBuilder._gen_mapping_strings(db_url, print_out = False)
    exec(script)
    return engine, meta, tables, session



class PrefixCategory(OrmClassBase):
    fields_sizes = []


    def __init__(self, type_name, bType, bTag):
        self.type_name = type_name
        self.bType = bType
        self.bTag = bTag



class PrefixType(OrmClassBase):
    fields_sizes = []


    def __init__(self, item_name, bType, bTag):
        self.item_name = item_name
        self.bType = bType
        self.bTag = bTag
