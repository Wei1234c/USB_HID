import universal_serial_bus
from orm.tools import AttrDict
from universal_serial_bus.legacy import CONTROL_REQUEST
from universal_serial_bus.orm import OrmClassBase



class HIDdevice(universal_serial_bus.USBdevice):
    HID_DESCRIPTOR_TYPE_CODE = 0x21
    REPORT_DESCRIPTOR_TYPE_CODE = 0x22
    PHYSICAL_DESCRIPTOR_TYPE_CODE = 0x23

    HID_DESCRIPTOR_TYPE_FIELD_IDX = 1
    REPORT_DESCRIPTOR_TYPE_FIELD_IDX = 6
    REPORT_DESCRIPTOR_SIZE_FIELD_IDX = 7
    CLASS_DESCRIPTOR_TYPES = AttrDict({'HID': 0x21, 'Report': 0x22, 'Physical': 0x23})

    CLASS_REQUEST_TYPES = AttrDict({'GET_REPORT'  : 0x01, 'SET_REPORT': 0x09,
                                    'GET_IDLE'    : 0x02, 'SET_IDLE': 0x0A,
                                    'GET_PROTOCOL': 0x03, 'SET_PROTOCOL': 0x0B})

    REPORT_TYPES = AttrDict({'Input': 0x01, 'Output': 0x02, 'Feature': 0x03})
    PROTOCOL_TYPES = AttrDict({'Boot': 0x00, 'Report': 0x01})


    @property
    def hid_version(self):
        return OrmClassBase.byte_array_to_bcd(self.hid_descriptors[0][2:4])


    @property
    def hid_descriptors(self):
        return [descriptor for descriptor in self.descriptors_from_config
                if descriptor[self.HID_DESCRIPTOR_TYPE_FIELD_IDX] == self.HID_DESCRIPTOR_TYPE_CODE]


    @property
    def report_descriptors(self):
        return [self.get_class_descriptor(descriptor_type = self.REPORT_DESCRIPTOR_TYPE_CODE, interface_idx = i)
                for i in range(len(self.hid_descriptors))]


    def get_class_descriptor(self, descriptor_type = HID_DESCRIPTOR_TYPE_CODE, physical_descriptor_idx = 0,
                             interface_idx = 0, wLength = 0x400, timeout = None):
        bmRequestType = CONTROL_REQUEST.DIRECTION.IN | CONTROL_REQUEST.RECIPIENT.INTERFACE | CONTROL_REQUEST.TYPE.STANDARD
        return self.ctrl_transfer(bmRequestType = bmRequestType,
                                  bRequest = CONTROL_REQUEST.GET_DESCRIPTOR,
                                  wValue = (descriptor_type << 8) | physical_descriptor_idx,
                                  wIndex = interface_idx,
                                  data_or_wLength = wLength, timeout = timeout)


    def set_class_descriptor(self, data, descriptor_type = HID_DESCRIPTOR_TYPE_CODE, physical_descriptor_idx = 0,
                             interface_idx = 0, timeout = None):
        bmRequestType = CONTROL_REQUEST.DIRECTION.OUT | CONTROL_REQUEST.RECIPIENT.INTERFACE | CONTROL_REQUEST.TYPE.STANDARD
        return self.ctrl_transfer(bmRequestType = bmRequestType,
                                  bRequest = CONTROL_REQUEST.SET_DESCRIPTOR,
                                  wValue = (descriptor_type << 8) | physical_descriptor_idx,
                                  wIndex = interface_idx,
                                  data_or_wLength = data, timeout = timeout)


    def get_class_request(self, request = CLASS_REQUEST_TYPES['GET_REPORT'], wValue = 0, interface_idx = 0,
                          wLength = 0x400, timeout = None):
        bmRequestType = CONTROL_REQUEST.DIRECTION.IN | 0x21
        return self.ctrl_transfer(bmRequestType = bmRequestType,
                                  bRequest = request,
                                  wValue = wValue,
                                  wIndex = interface_idx,
                                  data_or_wLength = wLength, timeout = timeout)


    def set_class_request(self, data, request = CLASS_REQUEST_TYPES['SET_REPORT'], wValue = 0, interface_idx = 0,
                          timeout = None):
        bmRequestType = CONTROL_REQUEST.DIRECTION.OUT | 0x21
        return self.ctrl_transfer(bmRequestType = bmRequestType,
                                  bRequest = request,
                                  wValue = wValue,
                                  wIndex = interface_idx,
                                  data_or_wLength = data, timeout = timeout)


    def get_report(self, report_type = REPORT_TYPES['Input'], report_id = 0, interface_idx = 0,
                   wLength = 0x400, timeout = None):
        return self.get_class_request(request = self.CLASS_REQUEST_TYPES['GET_REPORT'],
                                      wValue = (report_type << 8) | report_id,
                                      interface_idx = interface_idx,
                                      wLength = wLength, timeout = timeout)


    def set_report(self, data, report_type = REPORT_TYPES['Output'], report_id = 0, interface_idx = 0, timeout = None):
        return self.set_class_request(data,
                                      request = self.CLASS_REQUEST_TYPES['SET_REPORT'],
                                      wValue = (report_type << 8) | report_id,
                                      interface_idx = interface_idx,
                                      timeout = timeout)


    def get_idle(self, report_id = 0, interface_idx = 0, timeout = None):
        return self.get_class_request(request = self.CLASS_REQUEST_TYPES['GET_IDLE'],
                                      wValue = (0 << 8) | report_id,
                                      interface_idx = interface_idx,
                                      wLength = 1, timeout = timeout)


    def set_idle(self, duration = 0, report_id = 0, interface_idx = 0, timeout = None):
        return self.set_class_request(data = duration,
                                      request = self.CLASS_REQUEST_TYPES['SET_IDLE'],
                                      wValue = (duration << 8) | report_id,
                                      interface_idx = interface_idx,
                                      timeout = timeout)


    def get_protocol(self, interface_idx = 0, timeout = None):
        return self.get_class_request(request = self.CLASS_REQUEST_TYPES['GET_PROTOCOL'],
                                      wValue = 0,
                                      interface_idx = interface_idx,
                                      wLength = 1, timeout = timeout)


    def set_protocol(self, protocol_type = PROTOCOL_TYPES['Report'], interface_idx = 0, timeout = None):
        return self.set_class_request(data = None,
                                      request = self.CLASS_REQUEST_TYPES['SET_PROTOCOL'],
                                      wValue = protocol_type,
                                      interface_idx = interface_idx,
                                      timeout = timeout)
