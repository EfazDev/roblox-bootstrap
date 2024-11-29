#!/bin/bash

printMessage() {
    local message=$1
    echo "\033[38;5;202mRebuild EfazRobloxBootstrap @ ${message}\033[0m"
}

# Remove Existing EfazRobloxBootstrapMac.zip
printMessage "Removing Existing EfazRobloxBootstrapMacIntel.zip.."
rm -f ./Apps/EfazRobloxBootstrapMacIntel.zip

# Generate Hash
printMessage "Generating Main.py Hash.."
python3 ./Apps/Scripts/GenerateMainHash.py

# Build Pyinstaller Package
printMessage "Building Pyinstaller Package.."
pyinstaller ./Apps/Scripts/Pyinstaller/EfazRobloxBootstrap_macOSIntel.spec --distpath Apps --noconfirm

# Sign Package
printMessage "Signing Package.."

rm -rf ./Apps/EfazRobloxBootstrapMain.app/Contents/_CodeSignature/
sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapMain.app"
sudo xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapMain.app"
sudo xattr -cr "./Apps/EfazRobloxBootstrapMain.app"
sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapMain.app"

rm -rf ./Apps/EfazRobloxBootstrapLoad.app/Contents/_CodeSignature/
sudo xattr -dr com.apple.FinderInfo "./Apps/EfazRobloxBootstrapLoad.app"
sudo xattr -dr com.apple.metadata:_kMDItemUserTags "./Apps/EfazRobloxBootstrapLoad.app"
sudo xattr -cr "./Apps/EfazRobloxBootstrapLoad.app"
sudo codesign -s - --force --all-architectures --timestamp --deep "./Apps/EfazRobloxBootstrapLoad.app"

# Create EfazRobloxBootstrapMac.zip
printMessage "Creating EfazRobloxBootstrapMacIntel.zip.."
zip -r -y ./Apps/EfazRobloxBootstrapMacIntel.zip "./Apps/EfazRobloxBootstrapMain.app" "./Apps/Play Roblox.app" "./Apps/EfazRobloxBootstrapLoad.app" 

# Remove Build and EfazRobloxBootstrapLoad folder
printMessage "Partial Cleaning.."
rm -rf ./build/ ./Apps/EfazRobloxBootstrapLoad/ 

# Install EfazRobloxBootstrap
if [ "$1" != "installer" ]; then
    printMessage "Running Installer.."
    python3 Install.py --rebuild-mode
fi

# Clean Up Apps
printMessage "Cleaning Up.."
rm -rf ./Apps/EfazRobloxBootstrapMain.app/ ./Apps/EfazRobloxBootstrapLoad.app/ ./Apps/EfazRobloxBootstrapMain/ ./__pycache__/

# Done!
printMessage "Successfully rebuilt EfazRobloxBootstrap!"
printMessage "Check the Apps folder for the generated ZIP file! File: ./Apps/EfazRobloxBootstrapMacIntel.zip"
if [ "$1" != "installer" ]; then
    read -p "> "
fi