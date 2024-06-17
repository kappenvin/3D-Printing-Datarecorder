#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# qwiic_kx13x_ex1.py
#
# Simple example for the Qwiic KX132/4 Accelerometer
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, April 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2021 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
# A simple example for the kx132 showing asychronous data streaming i.e. continuous streaming.

from __future__ import print_function
import qwiic_kx13x
import time
import sys
import threading
import csv
from datetime import datetime

def convert(x):
    #convert the data for 8G range
    if x>8:
        x=x-16
    else:
        x=x

    return x

def runExample():

    print("\nSparkFun KX13X Accelerometer Example 1\n")
    myKx = qwiic_kx13x.QwiicKX134() 
    

    if myKx.connected == False:
            print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection", \
                    file=sys.stderr)
            return

    if myKx.begin():
        print("Ready.")
    else:
        print("Make sure you're using the KX132 and not the KX134")
    #print(hex(myKx.address))

    
    myKx.set_range(myKx.KX134_RANGE8G) # Update the range of the data output.
    myKx.initialize(myKx.DEFAULT_SETTINGS) # Load basic settings 
    #put sensor in standby mode to change the output data rate (written in the manual)
    myKx.accel_control(False)
    myKx.set_output_data_rate(12)
    myKx.accel_control(True)
    time.sleep(1)
    #should be 79 -->01001111
    print(myKx.get_output_data_rate())

    #print(hex(myKx.address)
    
    
    while True:
        myKx.get_accel_data()
        
        print("X: {0}g Y: {1}g Z: {2}g".format(convert(myKx.kx134_accel.x),
                                               convert(myKx.kx134_accel.y),
                                               convert(myKx.kx134_accel.z)))
        time.sleep(0.2) #Set delay to 1/Output Data Rate which is by default 50Hz 1/50 = .02

def save_accelerometer():

    myKx_1 = qwiic_kx13x.QwiicKX134(bus=1) 
    myKx_2 = qwiic_kx13x.QwiicKX134(bus=5)
    print(myKx_1._i2c)
    print(myKx_2._i2c)
    print(myKx_1._i2c)
    

    """
    if myKx.connected == False:
            print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection", \
                    file=sys.stderr)
            return
    """

    if myKx_1.begin():
        print("Ready.")
    else:
        print("Make sure you're using the KX132 and not the KX134")
    
    if myKx_2.begin():
        print("Ready.")
    else:
        print("Make sure you're using the KX132 and not the KX134")
    

    myKx_1.set_range(myKx_1.KX134_RANGE8G) # Update the range of the data output.
    myKx_1.initialize(myKx_1.DEFAULT_SETTINGS) # Load basic settings
    myKx_1.accel_control(False)
    myKx_1.set_output_data_rate(12)
    myKx_1.accel_control(True)
    
    
    myKx_2.set_range(myKx_1.KX134_RANGE8G) # Update the range of the data output.
    myKx_2.initialize(myKx_1.DEFAULT_SETTINGS) # Load basic settings
    myKx_2.accel_control(False)
    myKx_2.set_output_data_rate(12)
    myKx_2.accel_control(True)
    
    print(myKx_1.get_output_data_rate())
    print(myKx_2.get_output_data_rate())
    
    myKx_1.get_raw_accel_data()
    myKx_2.get_raw_accel_data()
    
    print(myKx_1.raw_output_data.y)
    print(myKx_2.raw_output_data.y)
    
    
    

    
    """
    #get the data and savae it with the microseconds to a csv file
    with open('accelerometer_data_kx1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Timestamp", "Velocity_X", "Velocity_Y", "Velocity_Z"])
        while True:
            myKx_1.get_accel_data()
            now = datetime.now()

            # Format datetime with milliseconds
            formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            accelerometer_data=[convert(myKx_1.kx134_accel.x),convert(myKx_1.kx134_accel.y),convert(myKx_1.kx134_accel.z),formatted_datetime]
            writer.writerow(accelerometer_data)
    """
    while True:
        
        
        myKx_1.get_accel_data()
        myKx_2.get_accel_data()
        
        print("Kx_1 X: {0}g Y: {1}g Z: {2}g".format(convert(myKx_1.kx134_accel.x),
                                               convert(myKx_1.kx134_accel.y),
                                               convert(myKx_1.kx134_accel.z)))
        
        time.sleep(1)
        
        
        print("KX_2 X: {0}g Y: {1}g Z: {2}g".format(convert(myKx_2.kx134_accel.x),
                                               convert(myKx_2.kx134_accel.y),
                                               convert(myKx_2.kx134_accel.z)))
        time.sleep(1) #Set delay to 1/Output Data Rate which is by default 50Hz 1/50 = .02
        
            
        

if __name__ == '__main__':
    save_accelerometer()
