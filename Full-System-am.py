import time
import board
import busio
import adafruit_am2320
import adafruit_dht
import glob
import RPi.GPIO as GPIO
import BlynkLib

#blynk
BLYNK_AUTH = 'j1N4LMcpA-eoW6VdbCqdwrtwPpXz3NO1'
blynk = BlynkLib.Blynk(BLYNK_AUTH)

tmr_start_time = time.time()

# am2315
i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)

# Dht22
dhtDevice = adafruit_dht.DHT22(board.D24)

#ds18b20
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

#mois
channel = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
 
def callback(channel):
        if GPIO.input(channel):
                print("No Water Detected!")
                blynk.virtual_write(2, "No Water Detected!")

        else:
                print("Water Detected!")
                blynk.virtual_write(3, "Water Detected!")
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

while True:
    blynk.run()
    print("Temperature: ", am.temperature)
    print("Humidity: ", am.relative_humidity)
    print(read_temp())
    blynk.virtual_write(4, "Temperature(AM) : " + str(am.temperature))
    blynk.virtual_write(5, "Humidity(AM) : " + str(am.relative_humidity))
    blynk.virtual_write(6, "Temperature Water : " + str(read_temp()))
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        blynk.virtual_write(0, "Temp : " + str(temperature_c))
        blynk.virtual_write(1, "Humidity : " + str(humidity))
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
