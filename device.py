#!watson/bin/python

import time
import sys
import pprint
import uuid
import signal
import json
import random


try:
	import ibmiotf.application
	import ibmiotf.device
	print('IBM Watson IoT modules sucessfylly imported!')
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device

# Quickstart credential.
organization = "quickstart"
deviceType = "MPU-6050"
deviceId = "847beb20bd6f"
authMethod = None
authToken = None

deviceOptions = {
	"org": organization, 
	"type": deviceType, 
	"id": deviceId, 
	"auth-method": authMethod, 
	"auth-token": authToken
}


# Handle Exit Signal
# Disconnect device from Watson IoT
def exitHandler(signal, frame):
	print('Exit!')
	deviceClient.disconnect()
	sys.exit(0)


if __name__ == "__main__":

	signal.signal(signal.SIGINT, exitHandler)

	print ("Device ID : " + deviceId)

	# Initialize the device client.
	try:
		deviceClient = ibmiotf.device.Client(deviceOptions)
		print('Watson Device Client sucessfully initialised') 
	except ibmiotf.ConnectionException  as e:
		print("Caught exception connecting device: %s" % str(e))

	# Connect device client.
	deviceClient.connect()


	while True:	
	
		# Acceleration generate random values (x, y, z)
		acceleration_x  = random.randint(0, 50)
		acceleration_y = random.randint(0, 50)
		acceleration_z = random.randint(0, 50)
		
		acceleration_data = { 'z': acceleration_z, 'y': acceleration_y, 'x': acceleration_x  }

		# Gyroscope generate random values (x, y, z)
		gyro_x  = random.randint(0, 180)
		gyro_y = random.randint(0, 180)
		gyro_z = random.randint(0, 180)

		gyroscope_data = {'z': gyro_z, 'y': gyro_y, 'x': gyro_x }


		# Combine Acceleration and Gyroscope values
		sensor_data = { 'acceleration': acceleration_data, 'gyro': gyroscope_data, }


		# Define device publish event callback.
		def OnPublishCallback():
			print("Watson confirm event received value is {}".format(sensor_data))

		# Post event to Watson IoT Platform
		success = deviceClient.publishEvent("MPU-6050 Sensor", "json", sensor_data, qos=0, on_publish=OnPublishCallback)
		
		if not success:
			print("Not connected to Watson IoT")


		time.sleep(1)