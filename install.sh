#!/bin/bash

# Dracula Installer - Vampire-DDOS-X
clear
echo -e "\e[1;35m[*] Initializing setup... \e[0m"
sleep 1

# Fix for Termux pip install restriction
fix_pip_for_termux() {
    if [ "$PREFIX" == "/data/data/com.termux/files/usr" ]; then
        echo -e "\e[1;33m[!] Termux detected. Trying to fix pip issue...\e[0m"
        curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py --break-system-packages 2>/dev/null || python3 get-pip.py --break-system-packages
        rm get-pip.py
    fi
}

# Check for command and install if missing
install_if_missing() {
    local pkg="$1"
    if ! command -v "$pkg" >/dev/null 2>&1; then
        echo -e "\e[1;36m[+] Installing $pkg...\e[0m"
        pkg install -y "$pkg" || apt install -y "$pkg"
    fi
}

# Update & upgrade system
apt update -y && apt upgrade -y

# Install core tools
install_if_missing python
install_if_missing python3
install_if_missing curl
install_if_missing git
install_if_missing tsu
install_if_missing figlet
install_if_missing toilet

# Termux-only fixes
fix_pip_for_termux

# Install pip packages
echo -e "\e[1;36m[+] Installing required Python modules...\e[0m"
pip install -r requirements.txt --break-system-packages 2>/dev/null || \
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || \
pip install colorama requests pysocks --break-system-packages || \
pip3 install colorama requests pysocks --break-system-packages

# Done
echo -e "\e[1;32m[✓] All dependencies installed successfully!\e[0m"
echo -e "\e[1;35m[!] You can now run: python3 vampire_ddos_x.py\e[0m"
