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
        self.loop = asyncio.new_event_loop()
        self.recording = False
        asyncio.set_event_loop(self.loop)

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
            print(f"An error occurred: {e}")
        print("Energy recording stopped")

    async def capture_power_data(self, interval, tapo_username, tapo_password, ip_address, filename):
        client = ApiClient(tapo_username, tapo_password)
        device = await client.p110(ip_address)
        try:
            with open(filename, 'a', newline="") as file:
                writer = csv.writer(file)
                energy_usage = await device.get_energy_usage()
                energy_data = energy_usage.to_dict()

                if file.tell() == 0:  # Check if the file is empty to write the header
                    writer.writerow(list(energy_data.keys()))

                while not self.stop_event.is_set():
                    energy_usage = await device.get_energy_usage()
                    energy_data = energy_usage.to_dict()

                    writer.writerow(list(energy_data.values()))
                    file.flush()

                    await asyncio.sleep(interval)

        except Exception as e:
            print(f"An error occurred during power data capture: {e}")

    def run_async(self, filename):
        self.loop.run_until_complete(self.capture_power_data(
            self.interval, self.tapo_username, self.tapo_password, self.ip_address, filename))
