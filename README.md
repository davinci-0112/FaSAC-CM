# FaSAC-CM

# DHT22
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2

# DS18b20
sudo raspi-config
# Select Interfacing Options
# Select 1-Wire
# Select Yes
sudo reboot
lsmod | grep -i w1_

# BH1750
sudo raspi-config
# Select Interfacing Options
# Select i2c
# Select Yes
sudo reboot
sudo pip3 install adafruit-circuitpython-bh1750

# Blynk relay
git clone https://github.com/WiringPi/WiringPi.git
cd wiringPi
./build
git clone https://github.com/blynkkk/blynk-library.git
cd blynk-library/linux
make clean all target=raspberry
./build.sh raspberry
sudo nano /etc/rc.local
/home/pi/blynk-library/linux/./blynk --token=Your token here

# AM2315
sudo raspi-config
# Select Interfacing Options
# Select i2c
# Select Yes
sudo reboot
sudo pip3 install adafruit-circuitpython-am2320
