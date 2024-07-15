import threading
import asyncio
import csv
from tapo import ApiClient


class p110_device:
    def __init__(self, tapo_username, tapo_password, ip_address, event, frequency=1):
        self.frequency = frequency
        self.interval = 1 / int(frequency)
        self.tapo_username = tapo_username
        self.tapo_password = tapo_password
        self.ip_address = ip_address
        self.stop_event = event
        self.recording = False
        self.client = ApiClient(tapo_username, tapo_password)

    def start(self, filename):
        """
        Start to record data in "filename"
        """
        print("Starting energy recording")
        self.t = threading.Thread(target=self.run_async, args=(filename,))
        self.t.start()
        self.recording = True
        print("Energy recording started")

    def stop(self, timeout=5):
        try:
            self.t.join(timeout=timeout)
        except Exception as e:
            print(f"An error occurred while stopping: {e}")
        print("Energy recording stopped")

    async def capture_power_data(self, interval, filename):
        try:
            self.device = await self.client.p110(self.ip_address)
            with open(filename, 'a', newline="") as file:
                writer = csv.writer(file)
                energy_usage = await self.device.get_energy_usage()
                energy_data = energy_usage.to_dict()

                if file.tell() == 0:  # Check if the file is empty to write the header
                    writer.writerow(list(energy_data.keys()))

                while not self.stop_event.is_set():
                    energy_usage = await self.device.get_energy_usage()
                    energy_data = energy_usage.to_dict()
                    
                    writer.writerow(list(energy_data.values()))
                    file.flush()

                    await asyncio.sleep(interval)

        except Exception as e:
            print(f"An error occurred during power data capture: {e}")

    def run_async(self, filename):
        try:
            asyncio.run(self.capture_power_data(self.interval, filename))
        except Exception as e:
            print(f"An error occurred in the energy event loop: {e}")
