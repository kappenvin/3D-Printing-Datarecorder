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
        self.loop = None  # Déplacer l'initialisation de l'event loop dans la méthode start

    async def start(self, filename):
        """
        Start to record data in "filename"
        """
        print("Starting energy recording")
        self.loop = asyncio.get_event_loop()
        
        self.task = self.loop.create_task(self.capture_power_data(
                self.interval, self.tapo_username, self.tapo_password, self.ip_address, filename))
        await self.task
        print("Energy recording started")

    async def stop(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
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
    # def run_async(self, filename):
    #     try:
    #         self.loop.run_until_complete(self.capture_power_data(
    #             self.interval, self.tapo_username, self.tapo_password, self.ip_address, filename))
    #     except Exception as e:
    #         print(f"An error occurred in the energy event loop: {e}")
    #     finally:
    #         self.loop.close()  # Ensure the loop is closed when done