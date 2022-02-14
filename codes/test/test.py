from usb_hid.orm.hid111 import HIDdevice


dev = HIDdevice(1118, 1915)  # MS mouse
rpt_descriptor = dev.report_descriptor_dbos[0].byte_array
print(dev.report_descriptor_dbos[0].parse())
# dev.close()