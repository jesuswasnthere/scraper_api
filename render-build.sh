#!/bin/bash

# Instalar Google Chrome en una carpeta accesible
echo "Instalando Google Chrome..."
mkdir -p $HOME/chrome && cd $HOME/chrome
wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_120.0.6099.230-1_amd64.deb
ar x google-chrome-stable_120.0.6099.230-1_amd64.deb
tar -xf data.tar.xz
mv usr/bin/google-chrome-stable $HOME/chrome/google-chrome

# Instalar ChromeDriver en la misma carpeta
echo "Instalando ChromeDriver..."
CHROME_VERSION=$(HOME/chrome/google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
wget -O chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver.zip
mv chromedriver $HOME/chrome/chromedriver
chmod +x $HOME/chrome/chromedriver

echo "Instalación completada."
