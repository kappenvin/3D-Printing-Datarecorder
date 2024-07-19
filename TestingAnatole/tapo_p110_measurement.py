import threading
# import pandas as pd
from datetime import datetime
import asyncio
import csv
from tapo import ApiClient


class p110_device:
    def __init__(self, tapo_username, tapo_password, ip_address, frequency=1):
        self.frequency = frequency
        self.interval = 1 / int(frequency)
        self.tapo_username = tapo_username
        self.tapo_password = tapo_password
        self.ip_address = ip_address
        self.stop_event = threading.Event()
        self.loop = asyncio.new_event_loop()
        self.recording = False
        asyncio.set_event_loop(self.loop)

    def start(self, filename):
        """
        Start to record data in "filename"
        """
        self.stop_event.clear()
        self.t = threading.Thread(target=self.run_async, args=(filename,))
        self.t.start()
        self.recording = True
        print("Energy recording started")

    def stop(self):
        self.stop_event.set()
        try:
            self.t.join()
        except Exception as e:
            print(f"An error occurred: {e}")
        print("Energy recording stopped")

    def run_async(self, filename):
        self.loop.run_until_complete(self.capture_data(
            self.interval, self.tapo_username, self.tapo_password, self.ip_address, filename))

    async def capture_data(self, interval, tapo_username, tapo_password, ip_address, filename):
        client = ApiClient(tapo_username, tapo_password)
        device = await client.p110(ip_address)
        try:
            with open(filename, 'a', newline="") as file:
                writer = csv.writer(file)
                energy_usage = await device.get_energy_usage()
                energy_data = energy_usage.to_dict()

                if file.tell() == 0:  # Check if the file is empty to write the header
                    writer.writerow(list(energy_data.keys()))

                print("1 dot = 1 measurement")
                while not self.stop_event.is_set():
                    energy_usage = await device.get_energy_usage()
                    energy_data = energy_usage.to_dict()

                    writer.writerow(list(energy_data.values()))
                    file.flush()

                    print(".", end="", flush=True)

                    await asyncio.sleep(interval)
        except Exception as e:
            print(f"An error occurred during data capture: {e}")
