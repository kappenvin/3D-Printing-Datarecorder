import sys
import time
import requests
import asyncio
import concurrent.futures
from datetime import datetime
import os
import qwiic_kx13x
import csv
from picamera2 import Picamera2, Preview
import board
import neopixel_spi as neopixel
import sys
import board
import adafruit_dht
import asyncio

import yaml  # To read the energy related code config file
import AnatoleCode.tapo_p110_measurement_pi as p110  # Power consumption monitoring


def convert(x):
    # convert the data for 8G range
    if x > 8:
        x = x-16
    else:
        x = x

    return x


def get_cotoprint_response(api_key="896D4E06F1454B9CA27511794B2AC7CD", octoprint_server="http://imi-octopi01.imi.kit.edu/api/job"):
    headers = {'X-Api-Key': api_key}

    try:
        response = requests.get(octoprint_server, headers=headers)
    except:
        print('no connection to server')

    if response.status_code == 200:
        data = response.json()
        return True, data
    else:
        print('Error:', response.status_code)
        return False, None

def run_asyncio(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)
    loop.close()

async def start_saving_power_consumption(energy_consumption_sensor, slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):

    settings_directory = os.path.join(directory_path, slicer_settings)
    # make directory Data/Anycubic/slicer_settings_standard
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Power_Consumption")
    os.makedirs(final_directory, exist_ok=True)
    final_path = os.path.join(final_directory, "power_consumption.csv")
    # start thread
    await energy_consumption_sensor.start(final_path)


async def save_accelerometer(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa", bus=1):
    settings_directory = os.path.join(directory_path, slicer_settings)
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Accelerometer")
    os.makedirs(final_directory, exist_ok=True)
    final_path = os.path.join(final_directory, f"accelerometer_data_bus{bus}.csv")

    myKx = qwiic_kx13x.QwiicKX134(bus=bus)

    if not myKx.connected:
        print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    if myKx.begin():
        print("Ready.")
    else:
        print("Make sure you're using the KX132 and not the KX134")

    myKx.initialize(myKx.DEFAULT_SETTINGS)
    myKx.set_range(myKx.KX134_RANGE8G)
    myKx.accel_control(False)
    myKx.set_output_data_rate(11)
    myKx.accel_control(True)

    with open(final_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Acceleration_X", "Acceleration_Y", "Acceleration_Z", "Timestamp"])
        while not my_event.is_set():
            myKx.get_accel_data()
            now = datetime.now()
            formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            accelerometer_data = [convert(myKx.kx134_accel.x), convert(myKx.kx134_accel.y), convert(myKx.kx134_accel.z), formatted_datetime]
            writer.writerow(accelerometer_data)


def save_images_picamera_thread(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(save_images_picamera(slicer_settings, part_name, directory_path))
    loop.close()

async def save_images_picamera(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (1720, 1280)}, controls={"ExposureTime": 3000})

    picam2.configure(config)
    await asyncio.sleep(2)
    picam2.start()

    pixels[1] = 0xFFFFFF
    pixels[2] = 0xFFFFFF
    pixels[3] = 0xFFFFFF
    pixels[4] = 0xFFFFFF
    pixels[5] = 0xFFFFFF
    pixels.show()

    settings_directory = os.path.join(directory_path, slicer_settings)
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Images")
    os.makedirs(final_directory, exist_ok=True)

    api_url = "http://imi-octopi01.imi.kit.edu//plugin/DisplayLayerProgress/values"

    while not my_event.is_set():
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        _, response = get_cotoprint_response(octoprint_server=api_url)
        layer = response["layer"]["current"]
        final_path = os.path.join(final_directory, current_time+"layer_"+layer+".jpg")
        picam2.capture_file(final_path)
        await asyncio.sleep(1)

    picam2.close()
    pixels.fill(0)
    pixels.show()


async def save_temperature(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):
    dhtDevice = adafruit_dht.DHT22(board.D12)

    settings_directory = os.path.join(directory_path, slicer_settings)
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Temperature_Humidity")
    os.makedirs(final_directory, exist_ok=True)
    final_path = os.path.join(final_directory, "temperature_humidity.csv")

    print(final_path)

    with open(final_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature", "Humidity"])
        print("writing")

        while not my_event.is_set():
            try:
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity

                print("humidity:", humidity)
                print(final_path)
                now = datetime.now()
                formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                data_temp_hum = [formatted_datetime, temperature_c, humidity]
                writer.writerow(data_temp_hum)
                file.flush()

            except RuntimeError as error:
                print("Error:", error.args[0])
                await asyncio.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                print(error)
                dhtDevice = adafruit_dht.DHT22(board.D12)

            await asyncio.sleep(2.0)



if __name__ == "__main__":
    NUM_PIXELS = 8
    PIXEL_ORDER = neopixel.GRB
    COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
    DELAY = 0.1

    spi = board.SPI()

    pixels = neopixel.NeoPixel_SPI(spi,
                                   NUM_PIXELS,
                                   pixel_order=PIXEL_ORDER,
                                   brightness=1.0,
                                   auto_write=False)

    initial_name = "start"
    started_a_while_ago = False
    stopped_printing_recently = False
    start_time = time.time()
    my_event = asyncio.Event()  # create an asyncio Event object

    # Initialize the connection to the power measurement device's API
    with open('AnatoleCode/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    async def main_loop():
        while True:
            operational, data = get_cotoprint_response()

            while not operational:
                operational, data = get_cotoprint_response()
                print("cant connect to octoprint")

            state = data["state"]
            name = data["job"]["file"]["name"]

            # get layer information
            api_url = "http://imi-octopi01.imi.kit.edu//plugin/DisplayLayerProgress/values"
            _, response = get_cotoprint_response(octoprint_server=api_url)
            layer = response["layer"]["current"]
            print(layer)
            if name != initial_name and state == "Printing" and layer != '_':
                if started_a_while_ago:
                    if not layer == "1":
                        print(f"Early start protection activated. state: {state}_{time.time()}")
                        await asyncio.sleep(1)
                        continue

                try:
                    slicer_settings_name, filename_pre = name.rsplit('_', 1)
                    filename_final, _ = os.path.splitext(filename_pre)

                    energy_consumption_sensor = p110.p110_device(config["sensor"]["current"]["username"],
                                                                 config["sensor"]["current"]["password"],
                                                                 config["sensor"]["current"]["ip"],
                                                                 my_event,
                                                                 config["sensor"]["current"]["frequency"])

                except ValueError:
                    slicer_settings_name, filename_pre = name, name

                my_event.clear()
                initial_name = name
                print("start measurements")

                loop = asyncio.get_event_loop()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    await loop.run_in_executor(executor, save_images_picamera_thread, slicer_settings_name, filename_final)

                await asyncio.gather(
                    save_accelerometer(slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa", 1),
                    save_accelerometer(slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa", 5),
                    start_saving_power_consumption(energy_consumption_sensor, slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa"),
                    save_temperature(slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa"),
                )

                started_a_while_ago = True
                stopped_printing_recently = False

            elif state != "Printing":
                if state == "Printing from SD":
                    print("Currently printing from SD card. Cannot perform measurements.")
                    await asyncio.sleep(5)
                    continue

                elif not started_a_while_ago or stopped_printing_recently:
                    print("Nothing is currently being printed.")
                    await asyncio.sleep(5)
                    continue

                print("stopping measurements")
                my_event.set()
                stopped_printing_recently = True
                initial_name = "start"

                await asyncio.sleep(5)
            else:
                print(f"state: {state}_{time.time()}")
                await asyncio.sleep(5)

    asyncio.run(main_loop())
