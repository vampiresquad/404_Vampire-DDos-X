#!/bin/bash

# Dracula's Installer for Vampire-DDOS-X [Coder :- ("Muhammad Shourov") ]
clear

# Banner
echo -e "\e[1;31m"
echo '██    ██  █████  ███    ███ ██████  ██ ██████  ███████     ██████  ██████  ███████ ██████  '
echo ' ██  ██  ██   ██ ████  ████ ██   ██ ██ ██   ██ ██          ██   ██ ██   ██ ██      ██   ██ '
echo '  ████   ███████ ██ ████ ██ ██████  ██ ██   ██ █████       ██████  ██████  █████   ██   ██ '
echo '   ██    ██   ██ ██  ██  ██ ██      ██ ██   ██ ██          ██   ██ ██      ██      ██   ██ '
echo '   ██    ██   ██ ██      ██ ██      ██ ██████  ███████     ██████  ██      ███████ ██████  '
echo -e "\e[1;32m                 Welcome to Vampire-DDOS-X Auto Installer (by Dracula)\e[0m\n"

sleep 1
echo -e "\e[1;33m[+] Updating packages...\e[0m"
apt update -y && apt upgrade -y

echo -e "\e[1;33m[+] Installing requirements (wget, unzip, python3)...\e[0m"
apt install wget unzip python3 -y

# Download release ZIP
echo -e "\e[1;36m[✓] Downloading tool from official Vampire Squad release...\e[0m"
wget -O 404_Vampire-DDos-X.zip https://github.com/vampiresquad/404_Vampire-DDos-X/releases/download/v1.0.0/404_Vampire-DDos-X-main.zip

# Extract and setup
echo -e "\e[1;36m[✓] Extracting tool files...\e[0m"
unzip 404_Vampire-DDos-X.zip > /dev/null
cd 404_Vampire-DDos-X-main || { echo -e "\e[1;31m[✘] Extraction failed!\e[0m"; exit 1; }

echo -e "\e[1;36m[✓] Setting permissions...\e[0m"
chmod +x install.sh || echo -e "\e[1;33m[!] install.sh not found or already executable\e[0m"

# Run install script
if [[ -f "install.sh" ]]; then
    echo -e "\e[1;35m[*] Running install.sh...\e[0m"
    bash install.sh
else
    echo -e "\e[1;31m[✘] install.sh not found. Skipping to main file...\e[0m"
fi

# Final run
if [[ -f "vampire-ddos-x.py" ]]; then
    echo -e "\e[1;32m[✔] Installation complete. Launching tool now...\e[0m"
    sleep 1
    python3 vampire-ddos-x.py
else
    echo -e "\e[1;31m[✘] Main file vampire-ddos-x.py not found!\e[0m"
    echo -e "\e[1;33m[!] Please check your extracted folder manually.\e[0m"
fi
