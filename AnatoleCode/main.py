"""
PrintingParametersOptimizer - main

Python program used to manage the 3D printer, its parameters
and the data generated. 
Trying to make something modular and
adaptable to different needs.

24/06 Anatole Martenne
"""
import os
import time
import yaml

import tapo_p110_measurement as p110

os.chdir('PrintingParametersOptimizer')
print(os.getcwd())
# Read config
with open('AnatoleCode/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
print(config)
# Set up data recorders

# Ensure the raspberry is working
input("Please start Raspberry recorder.\n\
      Press enter to continue...")
# Initialize the connection to the power measurement device's api
energy_consumption_sensor = p110.p110_device(config["sensor"]["current"]["username"],
                                             config["sensor"]["current"]["password"],
                                             config["sensor"]["current"]["ip"],
                                             config["sensor"]["current"]["frequency"])
print("Energy consumption sensor initialized")
print("Waiting for a print to begin...")

initial_name = "start"
while True:
    operational, data = get_octoprint_response()

    while not operational:
        operational, data = get_octoprint_response()
    state = data["state"]
    name = data["job"]["file"]["name"]

    # start measurement if the name changes otherwise let the measurement run
    if name != initial_name and state == "Printing":
        # slicer_settings_name,filename_pre=name.rsplit('_',1) # slicer_settings_standard_filename.gcode --> slicer_settings_standard , filename.gcode
        # filename.gcode --> filename , .gcode
        filename_final, _ = os.path.splitext(name)
        energy_consumption_sensor.start(filename_final+".csv")
        initial_name = name

        print("Started measuring")

    elif state != "Printing":
        if energy_consumption_sensor.recording:
            energy_consumption_sensor.stop()
            print("Stopped measuring")
            time.sleep(3)
            print("Waiting for a print to begin...")
