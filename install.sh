#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# Logo
echo -e "${BLUE}╔══════════════════════════════════════╗"
echo -e "${RED}║      Installing Vampire-DDOS-X       ║"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"

# Check if running in Termux or Linux
if [[ $PREFIX == *"com.termux"* ]]; then
    OS="termux"
    echo -e "${YELLOW}[+] Detected Termux environment${NC}"
else
    OS="linux"
    echo -e "${YELLOW}[+] Detected Linux environment${NC}"
fi

# Function to install packages with check
install_pkg() {
    for pkg in "$@"; do
        if ! command -v $pkg > /dev/null 2>&1; then
            echo -e "${YELLOW}[+] Installing missing package: $pkg${NC}"
            if [ "$OS" = "termux" ]; then
                pkg install -y $pkg
            else
                sudo apt install -y $pkg
            fi
        else
            echo -e "${GREEN}[✓] $pkg already installed${NC}"
        fi
    done
}

# Function to install python modules with pip
install_module() {
    for module in "$@"; do
        if ! python3 -c "import $module" 2>/dev/null; then
            echo -e "${YELLOW}[+] Installing Python module: $module${NC}"
            pip3 install $module || pip install $module
        else
            echo -e "${GREEN}[✓] Python module $module is installed${NC}"
        fi
    done
}

# Ensure Python3 and pip
echo -e "${YELLOW}[~] Checking Python & Pip...${NC}"
install_pkg python python3 curl wget git

# Fix Termux pip issue
if [ "$OS" = "termux" ]; then
    echo -e "${YELLOW}[~] Fixing pip in Termux...${NC}"
    curl -sS https://bootstrap.pypa.io/get-pip.py | python || true
fi

install_pkg tor

# Python pip install
install_pkg pip || true
pip3 install --upgrade pip

# Install Python dependencies
install_module colorama socks

# Permission fix
chmod +x vampire-ddos.py

# Final message
echo -e "${GREEN}"
echo "=============================================="
echo "  Vampire-DDOS-X Installed Successfully!"
echo -e "  ${CYAN}To Run The Tool:${NC} ${YELLOW}python3 vampire_ddos_x.py${NC}"
echo ""
echo "  Coded by: Muhammad Shourov (VAMPIRE)"
echo "=============================================="
echo -e "${NC}"
