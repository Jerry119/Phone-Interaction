import os
import csv

device_name = "emulator-5554"

command = "adb -s " + device_name + " shell "

os.system(command + "'date $currentTime' > phoneInfo.txt")
os.system(command + "dumpsys wifi | grep 'curState' >> phoneInfo.txt")
os.system(command + "dumpsys battery >> phoneInfo.txt")


os.system(command + "dumpsys telephony.registry | grep 'mSignalStrength' >> phoneInfo.txt")

lines = open("phoneInfo.txt", "r").read().split('\n')

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

battery_level = int(lines[14].split(':')[1])
wifi = lines[2].split('=')[1]
if wifi == 'InitialState':
    wifi_status = 'disabled/disconnected'
elif wifi == 'DisconnectedState':
    wifi_status = 'enabled/disconnected'
else:
    wifi_status = 'enabled/connected'
lte_strength = lines[19].split(': ')[1]
date = lines[0].split()
current_time = "{0:02d}".format(months.index(date[1]) + 1) + "-" + date[2] + "-" + date[5] + "-" + date[3]
powered = lines[5].rsplit(" ",1)[1]

status = ["Unknown", "Charging", "Discharging", "Not Charging", "Full"]
battery_status = status[int(lines[11].rsplit(' ', 1)[1])-1]

with open('phone_info.csv', mode='a+') as csv_file:
    fieldnames = ['Inspect Time', 'Plug In', 'Battery Status', 'Battery Level', 'WiFi status', 'LTE Signal Strength']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writerow({'Inspect Time': current_time, 'Plug In': powered, 'Battery Status': battery_status, 'Battery Level': battery_level, 'WiFi status': wifi_status, 'LTE Signal Strength': lte_strength})



