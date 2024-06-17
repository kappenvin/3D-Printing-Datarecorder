import time
import csv
import random
import datetime
import sys
import qwiic_kx13x

def measure_wait_time():
    start = time.perf_counter()
    myKx.get_raw_accel_data()  # Wait for 100 microseconds
    elapsed = time.perf_counter() - start
    print(f"Requested wait time was 0.0001 seconds (100 microseconds).")
    print(f"Measured wait time was {elapsed:.14f} seconds.")

myKx = qwiic_kx13x.QwiicKX134() 
    

if myKx.connected == False:
        print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection", \
                file=sys.stderr)

if myKx.begin():
    print("Ready.")
else:
    print("Make sure you're using the KX132 and not the KX134")
#print(hex(myKx.address))


myKx.set_range(myKx.KX134_RANGE8G) # Update the range of the data output.
myKx.initialize(myKx.DEFAULT_SETTINGS) # Load basic settings 
#put sensor in standby mode to change the output data rate (written in the manual)
myKx.accel_control(False)
myKx.set_output_data_rate(15)
myKx.accel_control(True)
measure_wait_time()
myKx.get_raw_accel_data()

