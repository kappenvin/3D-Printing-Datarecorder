from picamera2 import Picamera2, Preview
import time
from datetime import datetime
import os 
import argparse


'''
make directory and store images in it
duration: in minutes
input directory:/home/pi/Documents/Masterarbeit/Data/slicer_setting_test
partname: Art1

reslut direcotories: /home/pi/Documents/Masterarbeit/Data/slicer_setting_test/Art1/Images
#example usage 
# python picamera2_test_new.py /home/pi/Documents/Masterarbeit/Data/slicer_setting_test
'''

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('directory_path', type=str, help='The path to the directory where images will be saved')
parser.add_argument('partname', type=str, help='The path to the directory where images will be saved')
parser.add_argument('duration', type=str, help='The path to the directory where images will be saved')


args = parser.parse_args()

# Define the directory to save images
#save_directory = "/path/to/your/directory"

# Ensure the directory exists
os.makedirs(args.directory_path, exist_ok=True)
part_directory=os.path.join(args.directory_path,args.partname)
os.makedirs(part_directory,exist_ok=True)
final_directory=os.path.join(part_directory,"Images")
os.makedirs(final_directory,exist_ok=True)


duration=args.duration*60
for i in range(duration):
    # get the datetime
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    final_path=os.path.join(final_directory,current_time+".jpg")
    # save the file to the speicific directory 
    picam2.capture_file(final_path)
    time.sleep(1)

#example usage 
# python picamera2_test_new.py /home/pi/Documents/Masterarbeit/Data/slicer_setting_test



def save_images_picamera(directory_path,partname):
    '''
    make directory and store images in it
    input directory:/home/pi/Documents/Masterarbeit/Data/slicer_setting_test
    partname: Art1
    reslut direcotories: /home/pi/Documents/Masterarbeit/Data/slicer_setting_test/Art1/Images
    #example usage 
    # python picamera2_test_new.py /home/pi/Documents/Masterarbeit/Data/slicer_setting_test
    '''

    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    #picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)


    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)
    part_directory=os.path.join(directory_path,partname)
    os.makedirs(part_directory,exist_ok=True)
    final_directory=os.path.join(part_directory,"Images")
    os.makedirs(final_directory,exist_ok=True)


    duration=50*60
    for i in range(duration):
        # get the datetime
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        final_path=os.path.join(final_directory,current_time+".jpg")
        # save the file to the speicific directory 
        picam2.capture_file(final_path)
        # wait for 1 second to record the next image
        time.sleep(1)

