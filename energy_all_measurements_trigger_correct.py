import sys
import time
import requests
import threading
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
import cv2

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


def start_saving_power_consumption(energy_consumption_sensor, slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):

    settings_directory = os.path.join(directory_path, slicer_settings)
    # make directory Data/Anycubic/slicer_settings_standard
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Power_Consumption")
    os.makedirs(final_directory, exist_ok=True)
    final_path = os.path.join(final_directory, "power_consumption.csv")
    # start thread
    energy_consumption_sensor.start(final_path)


def save_accelerometer(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa", bus=1):

    settings_directory = os.path.join(directory_path, slicer_settings)
    # make directory Data/Anycubic/slicer_settings_standard
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Accelerometer")
    os.makedirs(final_directory, exist_ok=True)
    final_path = os.path.join(
        final_directory, f"accelerometer_data_bus{bus}.csv")

    myKx = qwiic_kx13x.QwiicKX134(bus=bus)

    if myKx.connected == False:
        print("The Qwiic KX13X Accelerometer device isn't connected to the system. Please check your connection",
              file=sys.stderr)
        return

    if myKx.begin():
        print("Ready.")
    else:
        print("Make sure you're using the KX132 and not the KX134")

    myKx.initialize(myKx.DEFAULT_SETTINGS)  # Load basic settings
    myKx.set_range(myKx.KX134_RANGE8G)  # Update the range of the data output.
    myKx.accel_control(False)
    myKx.set_output_data_rate(11)
    myKx.accel_control(True)

    # get the data and savae it with the microseconds to a csv file
    with open(final_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Acceleration_X", "Acceleration_Y",
                        "Acceleration_Z", "Timestamp"])
        while True:
            myKx.get_accel_data()
            now = datetime.now()

            # Format datetime with milliseconds
            formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            accelerometer_data = [convert(myKx.kx134_accel.x), convert(
                myKx.kx134_accel.y), convert(myKx.kx134_accel.z), formatted_datetime]
            writer.writerow(accelerometer_data)
            if my_event.is_set():
                break


def save_images_picamera(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):

    # check if the could be accessed
    picam2 = Picamera2()
    config = picam2.create_still_configuration(
        main={"size": (1720, 1280)}, controls={"ExposureTime": 3000})

    picam2.configure(config)
    time.sleep(2)
    picam2.start()

    pixels[1] = 0xFFFFFF
    pixels[2] = 0xFFFFFF
    pixels[3] = 0xFFFFFF
    pixels[4] = 0xFFFFFF
    pixels[5] = 0xFFFFFF
    # pixels[6]=0xFFFFFF
    pixels.show()

    # make the directories
    settings_directory = os.path.join(directory_path, slicer_settings)
    # make directory Data/Anycubic/slicer_settings_standard
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Images")
    os.makedirs(final_directory, exist_ok=True)

    api_url = "http://imi-octopi01.imi.kit.edu//plugin/DisplayLayerProgress/values"

    # get the image and save them
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # save the file to the speicific directory
        _, response = get_cotoprint_response(octoprint_server=api_url)
        layer = response["layer"]["current"]
        final_path = os.path.join(
            final_directory, current_time+"layer_"+layer+".jpg")
        picam2.capture_file(final_path)
        time.sleep(1)
        if my_event.is_set():
            picam2.close()
            pixels.fill(0)
            pixels.show()
            break


def save_temperature(slicer_settings="unknown", part_name="unknown", directory_path="/home/vincent/Documents/Data/Prusa"):

    dhtDevice = adafruit_dht.DHT22(board.D12)

    settings_directory = os.path.join(directory_path, slicer_settings)
    # make directory Data/Anycubic/slicer_settings_standard
    os.makedirs(settings_directory, exist_ok=True)
    part_directory = os.path.join(settings_directory, part_name)
    os.makedirs(part_directory, exist_ok=True)
    final_directory = os.path.join(part_directory, "Temperature_Humidity")
    os.makedirs(final_directory, exist_ok=True)
    final_path = os.path.join(final_directory, "temperature_humidity.csv")

    print(final_path)

    with open(final_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Timestamp", "Temperarture", "Humidity"])
        print("writing")

        while True:
            if my_event.is_set():
                dhtDevice.exit()
                break
            try:
                # Print the values to the serial port
                temperature_c = dhtDevice.temperature
                humidity = dhtDevice.humidity

                print("humidity:", humidity)
                print(final_path)
                now = datetime.now()

                # Format datetime with milliseconds
                formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                data_temp_hum = [formatted_datetime, temperature_c, humidity]
                writer.writerow(data_temp_hum)
                file.flush()

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print("Error:", error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                print(error)
                dhtDevice = adafruit_dht.DHT22(board.D12)

            time.sleep(2.0)


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
    # To avoid issues with new prints detected after the first one
    started_a_while_ago = False
    start_time = time.time()
    my_event = threading.Event()  # create an Event object

    # Initialize the connection to the power measurement device's api
    with open('AnatoleCode/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

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

        # start measurement if the name changes otherwise let the measurement run
        if name != initial_name and state == "Printing" and layer != '_':
            if started_a_while_ago:
                if not layer == "1":
                    print(f"Early start protection activated. state: {state}_{time.time()}")
                    continue

            try:
                # slicer_settings_standard_filename.gcode --> slicer_settings_standard , filename.gcode
                slicer_settings_name, filename_pre = name.rsplit('_', 1)
                # filename.gcode --> filename , .gcode
                filename_final, _ = os.path.splitext(filename_pre)

                energy_consumption_sensor = p110.p110_device(config["sensor"]["current"]["username"],
                                                             config["sensor"]["current"]["password"],
                                                             config["sensor"]["current"]["ip"],
                                                             my_event,
                                                             config["sensor"]["current"]["frequency"])

            except ValueError:
                slicer_settings_name, filename_pre = name, name

            # clear the event so that the code runs again
            my_event.clear()
            initial_name = name
            print("start measurements")
            t1 = threading.Thread(target=save_images_picamera, args=(
                slicer_settings_name, filename_final,))  # create t1 thread
            t2 = threading.Thread(target=save_accelerometer, args=(
                slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa", 1))
            t3 = threading.Thread(target=save_accelerometer, args=(
                slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa", 5))
            start_saving_power_consumption(
                energy_consumption_sensor, slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa")
            t4 = threading.Thread(target=save_temperature, args=(
                slicer_settings_name, filename_final, "/home/vincent/Documents/Data/Prusa"))
            # t5=threading.Thread(target = save_endoskop,args=(slicer_settings_name,filename_final,"/home/vincent/Documents/Data/Prusa"))
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            # t5.start()
            started_a_while_ago = True

        elif state != "Printing":
            if state == "Printing from SD":
                print("Currently printing from SD card. Cannot perform measurements.")
                time.sleep(5)
                continue
            print("stop measurement")
            my_event.set()
            try:
                print("wait for process 1")
                t1.join(timeout=5)
                print("wait for process 2")
                t2.join(timeout=5)
                print("wait for process 3")
                t3.join(timeout=5)
                print("wait for process 4")
                t4.join(timeout=5)
                energy_consumption_sensor.stop()
                # t5.join()
                initial_name = "start"
            except Exception as e:
                # Handle any exception that occurs
                print(f"An error occurred: {e}")

        else:
            print(f"state: {state}_{time.time()}")
            pass
