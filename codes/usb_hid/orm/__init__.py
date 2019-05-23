import universal_serial_bus
from universal_serial_bus.legacy import CONTROL_REQUEST



class HIDdevice(universal_serial_bus.USBdevice):
    DESCRIPTOR_TYPE_FIELD_IDX = 1
    DESCRIPTOR_TYPE_CODE = 0x21
    REPORT_DESCRIPTOR_TYPE_CODE = 0x22
    REPORT_DESCRIPTOR_TYPE_FIELD_IDX = 6
    REPORT_DESCRIPTOR_SIZE_FIELD_IDX = 7
    CLASS_DESCRIPTOR_TYPES = {'HID': 0x21, 'Report': 0x22, 'Physical': 0x23}


    @property
    def hid_descriptors(self):
        return [descriptor for descriptor in self.descriptors_from_config
                if descriptor[self.DESCRIPTOR_TYPE_FIELD_IDX] == self.DESCRIPTOR_TYPE_CODE]


    def get_class_descriptor(self, descriptor_type = DESCRIPTOR_TYPE_CODE, physical_descriptor_idx = 0,
                             interface_idx = 0, wLength = 0x400, timeout = None):
        return self.control_read(bRequest = CONTROL_REQUEST.GET_DESCRIPTOR,
                                 wValue = (descriptor_type << 8) | physical_descriptor_idx,
                                 wIndex = interface_idx,
                                 wLength = wLength, timeout = timeout,
                                 type = 0, recipient = CONTROL_REQUEST.RECIPIENT.CLASS)


    @property
    def report_descriptors(self):
        return [self.get_class_descriptor(descriptor_type = self.REPORT_DESCRIPTOR_TYPE_CODE, interface_idx = i)
                for i in range(len(self.hid_descriptors))]
