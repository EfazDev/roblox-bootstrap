#
# OrangeBlox Installer for Efaz's Roblox Bootstrap
#

import os
import sys
import shutil
import subprocess
import platform
import PyKits

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def isYes(text): return text.lower() == "y" or text.lower() == "yes" or text.lower() == "true" or text.lower() == "t"
def isNo(text): return text.lower() == "n" or text.lower() == "no" or text.lower() == "false" or text.lower() == "f"

current_path_location = os.path.dirname(os.path.abspath(__file__))
pip_class = PyKits.pip()
requests = PyKits.request()
main_os = platform.system()

printWarnMessage("--- Validating Requirements for OrangeBlox ---")
if not pip_class.osSupported(windows_build=17763, macos_version=(10,13,0)):
    if main_os == "Windows": printErrorMessage("OrangeBlox is only supported for Windows 10.0.17763 (October 2018) or higher. Please update your operating system in order to continue!")
    elif main_os == "Darwin": printErrorMessage("OrangeBlox is only supported for macOS 10.13 (High Sierra) or higher. Please update your operating system in order to continue!")
    input("> ")
    sys.exit(0)
if not pip_class.pythonSupported(3, 11, 0):
    if not pip_class.pythonSupported(3, 6, 0):
        printErrorMessage("Please update your current installation of Python above 3.11.0")
        input("> ")
        sys.exit(0)
    else:
        latest_python = pip_class.getLatestPythonVersion()
        printWarnMessage("--- Python Update Required ---")
        printMainMessage("Hello! In order to use OrangeBlox, you'll need to install Python 3.11 or higher in order to continue. ")
        printMainMessage(f"If you wish, you may install Python {latest_python} by typing \"y\" and continue.")
        printMainMessage("Otherwise, you will have to reinstall Efaz's Roblox Bootstrap to continue.")
        if isYes(input("> ")) == True:
            pip_class.pythonInstall(latest_python)
            latest_pip_class = PyKits.pip()
            latest_pip_class.ignore_same = True
            current_latest_python = latest_pip_class.getCurrentPythonVersion()
            if current_latest_python == latest_python:
                printSuccessMessage(f"Python has been installed correctly!")
                pip_class.restartScript("Main.py", sys.argv)
                sys.exit(0)
            else: printErrorMessage("Python Installation was may be canceled or Python was not installed!")
            input("> ")
printWarnMessage("--- Downloading OrangeBlox ---")
status = PyKits.ProgressBar()
class download_stat:
    def submit(self, info):
        if status: status.submit(f"[UPDATE] Downloading OrangeBlox!", int(info.percent))
requests.download("https://github.com/EfazDev/orangeblox/archive/refs/heads/main.zip", os.path.join(current_path_location, 'Update.zip'), submit_status=download_stat())
printWarnMessage("--- Preparing for OrangeBlox ---")
printMainMessage("Please wait while we prepare the update for the OrangeBlox install!")
zip_extract = pip_class.unzipFile(os.path.join(current_path_location, "Update.zip"), os.path.join(current_path_location, 'Update'), ["Main.py", "RobloxFastFlagsInstaller.py", "OrangeAPI.py", "Configuration.json", "Apps"])
if zip_extract.returncode == 0:
    for file in os.listdir(os.path.join(current_path_location, 'Update')):
        if file == "PipHandler.py" or file == "AppIcon.icns" or file == "AppIcon.ico":
            os.remove(os.path.join(current_path_location, 'Update', file))
    for file in os.listdir(os.path.join(current_path_location, 'Update')):
        src_path = os.path.join(os.path.join(current_path_location, 'Update'), file)
        dest_path = os.path.join(current_path_location, file)
        if os.path.isdir(src_path):
            try: pip_class.copyTreeWithMetadata(src_path, dest_path, dirs_exist_ok=True)
            except Exception as e: printDebugMessage(f"Update Error for directory ({src_path}): {str(e)}")
        else:
            if not file.endswith(".json"):
                try: shutil.copy2(src_path, dest_path)
                except Exception as e: printDebugMessage(f"Update Error for file ({src_path}): {str(e)}")
    printWarnMessage("--- Running Install for OrangeBlox ---")
    printMainMessage("Please wait while we start the OrangeBlox installer!")
    silent_install = subprocess.run(args=([sys.executable, "Install.py"] if "-s" in sys.argv else [sys.executable, "Install.py", "--update-mode"]), cwd=current_path_location)
    if not (silent_install.returncode == 0): printErrorMessage("Bootstrap Installer failed.")
else: printErrorMessage("Something went wrong!")