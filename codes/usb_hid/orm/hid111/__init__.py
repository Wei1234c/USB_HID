from universal_serial_bus.orm.usb20.descriptors import *
from .descriptors import *
from .descriptors import HidDescriptor
from .. import HIDdevice


int_eq_hex = OrmClassBase.int_eq_hex
int_to_hex = OrmClassBase.int_to_hex



class HIDdevice(HIDdevice):

    @classmethod
    def _categorize(cls, descriptor, intf_type = None):

        _class = None

        if int_eq_hex(descriptor[1], '01'):  # 如果是 device
            _class = StandardDeviceDescriptor

        if int_eq_hex(descriptor[1], '02'):  # 如果是 config
            _class = StandardConfigurationDescriptor

        if int_eq_hex(descriptor[1], '05'):  # 如果是 endpoint
            _class = StandardEndpointDescriptor

        if int_eq_hex(descriptor[1], '04'):  # 如果是 interface
            _class = StandardInterfaceDescriptor

            if int_eq_hex(descriptor[5], '03'):  # 如果是 HID
                intf_type = "HID"

        if int_eq_hex(descriptor[1], '21'):  # 如果是 HID descriptor
            _class = HidDescriptor

        return _class, intf_type


    @property
    def hid_descriptor_dbos(self):
        return [HidDescriptor.from_byte_array(descriptor) for descriptor in self.hid_descriptors]
