import asyncio
import csv
from tapo import ApiClient


class P110Device:
    def __init__(self, tapo_username, tapo_password, ip_address, frequency=1):
        self.frequency = frequency
        self.interval = 1 / int(frequency)
        self.tapo_username = tapo_username
        self.tapo_password = tapo_password
        self.ip_address = ip_address
        self.recording = False

    def start(self, filename):
        print("Starting energy recording")
        self.recording = True
        loop = asyncio.get_event_loop()
        loop.create_task(self.capture_power_data(filename))

    def stop(self):
        self.recording = False
        loop = asyncio.get_event_loop()
        loop.stop()

    async def capture_power_data(self, filename):
        try:
            async with ApiClient(self.tapo_username, self.tapo_password) as client:
                while self.recording:
                    try:
                        device = await client.p110(self.ip_address)
                        with open(filename, 'a', newline="") as file:
                            writer = csv.writer(file)
                            if file.tell() == 0:  # Check if the file is empty to write the header
                                writer.writerow(list(device.get_energy_usage().to_dict().keys()))

                            energy_data = await device.get_energy_usage().to_dict()
                            writer.writerow(list(energy_data.values()))
                            file.flush()
                    except Exception as e:
                        print(f"Error during power data capture: {e}")
                    await asyncio.sleep(self.interval)
        except Exception as e:
            print(f"Failed to connect to Tapo API: {e}")
        finally:
            print("Stopping power data capture.")
