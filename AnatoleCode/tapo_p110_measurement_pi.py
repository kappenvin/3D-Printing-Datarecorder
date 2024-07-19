import asyncio
import csv
from tapo import ApiClient
import time

class p110_device:
    def __init__(self, tapo_username, tapo_password, ip_address, event, frequency=1):
        self.frequency = frequency
        self.interval = 1 / int(frequency)
        self.tapo_username = tapo_username
        self.tapo_password = tapo_password
        self.ip_address = ip_address
        self.stop_event = event

    async def start(self, filename):
        """
        Start to record data in "filename"
        """
        print("Starting energy recording")
        capture_task = await self.capture_power_data(
                self.interval, self.tapo_username, self.tapo_password, self.ip_address, filename)

        print("Energy recording started")
                
    async def capture_power_data(self, interval, tapo_username, tapo_password, ip_address, filename):
        client = ApiClient(tapo_username, tapo_password)
        try:
            device = await asyncio.wait_for(client.p110(ip_address), timeout=1) 
        except Exception as e:
            print(e)
        try:
            with open(filename, 'a', newline="") as file:
                writer = csv.writer(file)
                try:
                    energy_usage = await asyncio.wait_for(device.get_energy_usage(), timeout=0.2)
                except Exception as e:
                    print(e)
                energy_data = energy_usage.to_dict()

                if file.tell() == 0:  # Check if the file is empty to write the header
                    writer.writerow(list(energy_data.keys()))

                while not self.stop_event.is_set():
                    try:
                        print("s")
                        energy_usage = await asyncio.wait_for(device.get_energy_usage(), timeout=0.2)
                        print("r")
                        energy_data = energy_usage.to_dict()
                        
                        writer.writerow(list(energy_data.values()))
                        file.flush()
                    except Exception as e:
                        print(e)
                    await asyncio.sleep(interval)

                print("Energy recording stopped")

        except Exception as e:
            print(f"An error occurred during power data capture: {e}")
