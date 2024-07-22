import asyncio
import csv
# from tapo import ApiClient
from PyP100 import PyP110
import time

class p110_device:
    def __init__(self, tapo_username, tapo_password, ip_address, event, frequency=1):
        self.frequency = frequency
        self.interval = 1 / int(frequency)
        self.tapo_username = tapo_username
        self.tapo_password = tapo_password
        self.ip_address = ip_address
        self.stop_event = event
        self.p110 = PyP110.P110(self.ip_address, self.tapo_username, self.tapo_password)

    async def capture_power_data(self, filename):
        print("Starting energy recording")

        # client = ApiClient(self.tapo_username, self.tapo_password)
        # device = await client.p110(self.ip_address)
        try:
            with open(filename, 'a', newline="") as file:
                writer = csv.writer(file)
                try:
                    energy_data = self.p110.getEnergyUsage()
                    print("energy_data=",energy_data)
                except Exception as e:
                    print(e)
                # energy_data = energy_usage.to_dict()
                

                if file.tell() == 0:  # Check if the file is empty to write the header
                    writer.writerow(list(energy_data.keys()))

                print("Energy recording started")
                while not self.stop_event.is_set():
                    try:
                        print("s")
                        energy_data = self.p110.getEnergyUsage()
                        print("r")
                        # energy_data = energy_usage.to_dict()
                        
                        writer.writerow(list(energy_data.values()))
                        file.flush()
                    except Exception as e:
                        print(e)
                    await asyncio.sleep(self.interval)
                print("Energy recording stopped")

        except Exception as e:
            print(f"An error occurred during power data capture: {e}")