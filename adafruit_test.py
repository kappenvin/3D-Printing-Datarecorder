import time
import board
import adafruit_dht
import csv
from datetime import datetime

# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D12)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)



def save_temperature():
    
    dhtDevice = adafruit_dht.DHT22(board.D12)
    
    final_path="test.csv"
    
    with open(final_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Timestamp", "Temperarture", "Humidity"])
        print("writing")
            
        while True:
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity
                
                print("humidity:", humidity)
                print(final_path)
                now = datetime.now()

                # Format datetime with milliseconds
                formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                data_temp_hum=[formatted_datetime,temperature_c,humidity]
                writer.writerow(data_temp_hum)

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print("Error:",error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                #dhtDevice.exit()
                print(error)

            time.sleep(2.0)



save_temperature()