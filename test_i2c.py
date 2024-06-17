import qwiic_i2c
import sys

# Linux (Raspberry Pi) - Specify I2C bus index
my_bus = qwiic_i2c.get_i2c_driver(iBus = 1)

scan_list = my_bus.scan()
print("Bus scan:", scan_list)

ping_result = my_bus.ping(0x1E)
print("Device is connected:", ping_result)

read_data = my_bus.readByte(0x1E, 0x13)

print("Read byte:", read_data)
print(0x46)

print(qwiic_i2c.isDeviceConnected(0x1F))