#############################################################
# This program is for
#
#
#
#############################################################

# Over X-amount of time, record average weather information
# and number of times motion was detected. Reset motion per x time.

# Libraries to Import
import RPi.GPIO as GPIO
from Adafruit_BME280 import *

import time
import threading

# Set up GPIO pins for reading in digital I/O
ir_input = 11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO ir_input set up as input. It is pulled up to stop false signals
GPIO.setup(ir_input, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables to use
global humid_arr
humid_arr = []
global temp_arr
temp_arr = []
global press_arr
press_arr = []
global num_ppl_count
num_ppl_count = 0
global acq_BME280_delay
acq_BME280_delay = 0.5
global send_data_time
send_data_time = 60


class AcquireData:

    def __init__(self):
        # Initialize a lock object
        global lock
        lock = threading.Lock()
        # Initialize separate threads to run
        global t_BME280
        t_BME280 = threading.Thread(target=self.acq_Weather)
        global t_IR_trip
        t_IR_trip = threading.Thread(target=self.acq_IR_trip)
        global t_sendData
        t_sendData = threading.Thread(target=self.store_Data)
        t_BME280.start()
        t_IR_trip.start()
        t_sendData.start()
        t_BME280.join()
        t_IR_trip.join()
        t_sendData.join()

    def acq_Weather(self):
        # Acquire weather information
        # Setup sensor to acquire data
        sensor = BME280('BME280_OSAMPLE_8', 'BME280_OSAMPLE_2', 'BME280_OSAMPLE_1', 'BME280_FILTER_16')
        # Initialize counter
        ii = 0

        # Initialize infinite while loop for acquire data
        while True:
            # Acquire temperature in celsius
            temp_arr[ii] = sensor.read_temperature()
            # Acquire pressure but convert to hectopascals
            pascals = sensor.read_pressure()
            press_arr[ii] = pascals / 100
            # Acquire humidity as a percentage
            humid_arr[ii] = sensor.read_humidity()

            # Increase counter
            ii += 1

            # Delay acquisition for specified time
            time.sleep(acq_BME280_delay)
            break


    def acq_IR_trip(self):
        while True:
            try:
                GPIO.wait_for_edge(ir_input, GPIO.FALLING)
                # Increase the counter for every time pin value is 1
                num_ppl_count += 1
            except:
                pass
            break


    def store_Data(self):
        # Wait specific amount of time before storing data
        time.sleep(send_data_time)
        # Lock other threads
        lock.acquire()

        # Initialize connection to database

        # Compute average weather information
        ave_temp = sum(temp_arr)/float(len(temp_arr))
        ave_humid = sum(humid_arr) / float(len(humid_arr))
        ave_press = sum(press_arr) / float(len(press_arr))

        # Send data to database
        print(ave_temp)
        # Reset global variables
        num_ppl_count = 0
        temp_arr.clear()
        humid_arr.clear()
        press_arr.clear()

        # Release lcok
        lock.release()

if __name__ == '__main__':
    start = AcquireData()
    start.run()
