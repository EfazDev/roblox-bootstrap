import shutil
import os
import platform
import json
import subprocess
import time
import sys
import RobloxFastFlagsInstaller
from PipHandler import pip

def printMainMessage(mes): print(f"\033[38;5;255m{mes}\033[0m")
def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
def printSuccessMessage(mes): print(f"\033[38;5;82m{mes}\033[0m")
def printWarnMessage(mes): print(f"\033[38;5;202m{mes}\033[0m")
def printYellowMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")
def printDebugMessage(mes): print(f"\033[38;5;226m{mes}\033[0m")

def isYes(text): return text.lower() == "y" or text.lower() == "yes"
def isNo(text): return text.lower() == "n" or text.lower() == "no"
def isRequestClose(text): return text.lower() == "exit" or text.lower() == "exit()"
def is_x86_windows():
    if platform.system() == "Windows":
        if platform.architecture()[0] == "32bit":
            return True
    return False
def copy_with_symlinks(src, dest, ignore_files=[]):
    if os.path.exists(src):
        try:
            for i in ignore_files:
                if i in src:
                    return
            if os.path.lexists(dest):
                if os.path.isdir(dest) and not os.path.islink(dest):
                    pass
                else:
                    os.remove(dest)
            if os.path.islink(src):
                os.symlink(os.readlink(src), dest)
            elif os.path.isdir(src):
                os.makedirs(dest, exist_ok=True)
                for item in os.listdir(src):
                    if item in ignore_files:
                        continue
                    copy_with_symlinks(os.path.join(src, item), os.path.join(dest, item))
            else:
                shutil.copy2(src, dest)
        except Exception as e:
            printDebugMessage(f"An error occurred while transferring a file, a reinstallation may be needed: {str(e)}")

if __name__ == "__main__":
    main_os = platform.system()
    stored_main_app = {
        "Darwin": ["/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app", "/Applications/EfazRobloxBootstrap.app", "/Applications/Play Roblox.app"],
        "Windows": [os.path.join(f"{os.getenv('LOCALAPPDATA')}", "EfazRobloxBootstrap"), os.path.join(f"{os.getenv('LOCALAPPDATA')}", "EfazRobloxBootstrap", "EfazRobloxBootstrap.exe"), os.path.join(f"{os.getenv('LOCALAPPDATA')}", "EfazRobloxBootstrap")]
    }
    ignore_files = ["build", "__pycache__", "LICENSE", "README.md", "InstallPython.sh", "FastFlagConfiguration.json", ".git"]
    current_version = {"version": "1.3.8"}
    current_path_location = os.path.dirname(os.path.abspath(__file__))
    instant_install = False
    silent_mode = False
    rebuild_mode = False
    use_x86_windows = False
    disable_remove_other_operating_systems = False
    disabled_url_scheme_installation = None
    disabled_shortcuts_installation = None
    use_installation_syncing = True
    disable_download_for_app = True
    remove_unneeded_messages = True
    pip_class = pip()

    handler = RobloxFastFlagsInstaller.Main()
    def ignore_files_func(dir, files): return set(ignore_files) & set(files)

    if "--rebuild-mode" in sys.argv:
        rebuild_mode = True
        disable_remove_other_operating_systems = True
        instant_install = True
    else:
        if "--install" in sys.argv:
            instant_install = True
        if "--silent" in sys.argv:
            silent_mode = True
            def printMainMessage(mes): silent_mode = True
            def printErrorMessage(mes): print(f"\033[38;5;196m{mes}\033[0m")
            def printSuccessMessage(mes): silent_mode = True
            def printWarnMessage(mes): silent_mode = True
            def printDebugMessage(mes): silent_mode = True
        else:
            if not ("--no-clear" in sys.argv): os.system("cls" if os.name == "nt" else 'echo "\033c\033[3J"; clear')
        if "--disable-remove" in sys.argv:
            disable_remove_other_operating_systems = True
    if "--disable-installation-sync" in sys.argv:
        use_installation_syncing = False
    if "--enable-unneeded-messages" in sys.argv:
        remove_unneeded_messages = False
    if "--disable-url-schemes" in sys.argv:
        disabled_url_scheme_installation = True
    if "--disable-shortcuts" in sys.argv:
        disabled_shortcuts_installation = True
    if "--use-x86-windows" in sys.argv:
        use_x86_windows = True

    printWarnMessage("-----------")
    printWarnMessage("Welcome to Efaz's Roblox Bootstrap Installer!")
    printWarnMessage("Made by Efaz from efaz.dev!")
    printWarnMessage(f"v{current_version['version']}")
    printWarnMessage("-----------")
    # Requirement Checks
    if main_os == "Windows":
        printMainMessage(f"System OS: {main_os}")
        found_platform = "Windows"
    elif main_os == "Darwin":
        printMainMessage(f"System OS: {main_os} (macOS)")
        found_platform = "Darwin"
    else:
        printErrorMessage("Efaz's Roblox Bootstrap is only supported for macOS and Windows.")
        input("> ")
        sys.exit(0)
    current_python_version = platform.python_version_tuple()
    if current_python_version < ("3", "10", "0"):
        printErrorMessage("Please update your current installation of Python above 3.10.0")
        input("> ")
        sys.exit(0)
    else:
        printMainMessage(f"Python Version: {platform.python_version()}")
    if main_os == "Windows":
        installation_folder = f"{handler.getRobloxInstallFolder()}\\"
        if not os.path.exists(installation_folder):
            printErrorMessage("Please install Roblox from the Roblox website in order to use this bootstrap!")
            input("> ")
            sys.exit(0)
        else:
            cur_vers = handler.getCurrentClientVersion()
            if cur_vers["success"] == True:
                printMainMessage(f"Current Roblox Version: {cur_vers['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
    elif main_os == "Darwin":
        if os.path.exists("/Applications/Roblox.app/"):
            cur_vers = handler.getCurrentClientVersion()
            if cur_vers["success"] == True:
                printMainMessage(f"Current Roblox Version: {cur_vers['version']}")
            else:
                printErrorMessage("Something went wrong trying to determine your current Roblox version.")
                input("> ")
                sys.exit(0)
        else:
            printErrorMessage("Please install Roblox from the Roblox website in order to use this bootstrap!")
            input("> ")
            sys.exit(0)
    printMainMessage(f"Installation Folder: {current_path_location}")
    overwrited = False
    if os.path.exists(stored_main_app[found_platform][0]) and os.path.exists(stored_main_app[found_platform][1]):
        overwrited = True
    def install():
        global disabled_url_scheme_installation
        global use_x86_windows
        global disable_remove_other_operating_systems
        global disabled_shortcuts_installation
        global disable_download_for_app
        global use_installation_syncing

        try:
            import requests
            import plyer
            import pypresence
            if main_os == "Darwin":
                import posix_ipc
                import objc
                import tkinter
            elif main_os == "Windows":
                import win32com.client # type: ignore
        except Exception as e:
            printMainMessage("Some modules are not installed and may be needed for some features. Do you want to install all the modules needed now? (y/n)")
            if instant_install == True or isYes(input("> ")) == True:
                pip_class.install(["requests", "plyer", "pypresence"])
                if main_os == "Darwin":
                    pip_class.install(["posix-ipc", "pyobjc", "tk"])
                elif main_os == "Windows":
                    pip_class.install(["pywin32"])
                import requests
                import plyer
                import pypresence
                if main_os == "Darwin":
                    import posix_ipc
                    import objc
                    import tkinter
                elif main_os == "Windows":
                    import win32com.client # type: ignore
                printSuccessMessage("Successfully installed modules!")
            else:
                printErrorMessage("Ending installation..")
                sys.exit(0)
        if os.path.exists(f"{current_path_location}/Apps/"):
            if main_os == "Darwin":
                if os.path.exists(f"{current_path_location}/Apps/EfazRobloxBootstrapMac.zip"):
                    # Unzip Installation ZIP
                    printMainMessage("Unzipping Installation ZIP File..")
                    try:
                        subprocess.run(["unzip", "-o", f"{current_path_location}/Apps/EfazRobloxBootstrapMac.zip", "-d", f"{current_path_location}/Apps/EfazRobloxBootstrapMac"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    except Exception as e:
                        printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                    time.sleep(1)
                else:
                    printYellowMessage("Something went wrong finding EfazRobloxBootstrapMac.zip. It will require a EfazRobloxBootstrapMac folder in order for installation to finish.")
                if os.path.exists(f"{current_path_location}/Apps/EfazRobloxBootstrapMac/"):
                    # Get FastFlagConfiguration.json Data
                    if overwrited == True:
                        printMainMessage("Getting Configuration File Data..")
                        fast_config_path = os.path.join(stored_main_app[found_platform][0], "Contents", "Resources", "FastFlagConfiguration.json")
                        if os.path.exists(fast_config_path):
                            with open(fast_config_path, "r") as f:
                                fastFlagConfig = json.load(f)
                        else:
                            fastFlagConfig = {}
                    else:
                        fastFlagConfig = {}

                    # Delete Other Operating System Files
                    if not (disable_remove_other_operating_systems == True or fastFlagConfig.get("EFlagDisableDeleteOtherOSApps") == True):
                        deleted_other_os = False
                        if os.path.exists(f"{current_path_location}/Apps/EfazRobloxBootstrapWindows.zip"):
                            os.remove(f"{current_path_location}/Apps/EfazRobloxBootstrapWindows.zip")
                            deleted_other_os = True
                        if deleted_other_os == True: printMainMessage("To help save space, the script has automatically deleted files made for other operating systems!")

                    # Insert New Display Names
                    printMainMessage("Adding Display Names..")
                    if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Info.plist"):
                        dis = handler.readPListFile("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Info.plist")
                        dis["CFBundleDisplayName"] = "Efaz's Roblox Bootstrap"
                        dis["CFBundleShortVersionString"] = current_version["version"]
                        dis["CFBundleVersion"] = current_version["version"]
                        handler.writePListFile("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Info.plist", dis)
                    if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Info.plist"):
                        dis = handler.readPListFile("/Applications/EfazRobloxBootstrap.app/Contents/Info.plist")
                        dis["CFBundleDisplayName"] = "Efaz's Roblox Bootstrap"
                        dis["CFBundleShortVersionString"] = current_version["version"]
                        dis["CFBundleVersion"] = current_version["version"]
                        handler.writePListFile("/Applications/EfazRobloxBootstrap.app/Contents/Info.plist", dis)
                    if os.path.exists("/Applications/Play Roblox.app/Contents/Info.plist"):
                        dis = handler.readPListFile("/Applications/Play Roblox.app/Contents/Info.plist")
                        dis["CFBundleDisplayName"] = "Play Roblox"
                        dis["CFBundleShortVersionString"] = current_version["version"]
                        dis["CFBundleVersion"] = current_version["version"]
                        handler.writePListFile("/Applications/Play Roblox.app/Contents/Info.plist", dis)

                    # Remove Old Versions of Loader
                    if os.path.exists("/Applications/EfazRobloxBootstrapLoader.app/"):
                        printMainMessage("Removing Older Versions of Bootstrap Loader..")
                        shutil.rmtree("/Applications/EfazRobloxBootstrapLoader.app/")
                    elif os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/EfazRobloxBootstrap.app/"):
                        printMainMessage("Removing Older Versions of Bootstrap Loader..")
                        shutil.rmtree("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/EfazRobloxBootstrap.app/")
                    
                    # Remove Installed Loader
                    if os.path.exists(stored_main_app[found_platform][0]):
                        try:
                            printMainMessage("Removing Installed Bootstrap Loader..")
                            shutil.rmtree(stored_main_app[found_platform][0])
                        except Exception as e:
                            printErrorMessage("Something went wrong removing installed bootstrap loader!")

                    # Delete frameworks if there's extra
                    printMainMessage("Clearing App Frameworks..")
                    if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Frameworks/"):
                        shutil.rmtree("/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz\'s Roblox Bootstrap.app/Contents/Frameworks/")
                    if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Frameworks/"):
                        shutil.rmtree("/Applications/EfazRobloxBootstrap.app/Contents/Frameworks/")
                    if os.path.exists("/Applications/Play Roblox.app/Contents/Frameworks/"):
                        shutil.rmtree("/Applications/Play Roblox.app/Contents/Frameworks/")

                    # Convert All Mod Modes to Mods
                    if os.path.exists(f"{current_path_location}/ModModes/"):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(f"{current_path_location}/ModModes/"):
                            mod_mode_path = os.path.join(f"{current_path_location}/ModModes/", i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(f"{current_path_location}/Mods/{i}/"):
                                    os.makedirs(f"{current_path_location}/Mods/{i}/", exist_ok=True)
                                shutil.copytree(mod_mode_path, f"{current_path_location}/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree(f"{current_path_location}/ModModes/")
                    if os.path.exists("/Applications/EfazRobloxBootstrap.app/Contents/Resources/ModModes/"):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir("/Applications/EfazRobloxBootstrap.app/Contents/Resources/ModModes/"):
                            mod_mode_path = os.path.join("/Applications/EfazRobloxBootstrap.app/Contents/Resources/ModModes/", i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(f"/Applications/EfazRobloxBootstrap.app/Contents/Resources/Mods/{i}/"):
                                    os.makedirs(f"/Applications/EfazRobloxBootstrap.app/Contents/Resources/Mods/{i}/", exist_ok=True)
                                shutil.copytree(mod_mode_path, f"/Applications/EfazRobloxBootstrap.app/Contents/Resources/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree("/Applications/EfazRobloxBootstrap.app/Contents/Resources/ModModes/")
                    
                    # Install to /Applications/
                    printMainMessage("Installing to Applications Folder..")
                    copy_with_symlinks(f"{current_path_location}/Apps/EfazRobloxBootstrapMac/Apps/EfazRobloxBootstrapLoad.app", stored_main_app[found_platform][1])
                    if os.path.exists(stored_main_app[found_platform][0]):
                        copy_with_symlinks(f"{current_path_location}/Apps/EfazRobloxBootstrapMac/Apps/EfazRobloxBootstrapMain.app", stored_main_app[found_platform][0], ignore_files=ignore_files)
                    else:
                        copy_with_symlinks(f"{current_path_location}/Apps/EfazRobloxBootstrapMac/Apps/EfazRobloxBootstrapMain.app", stored_main_app[found_platform][0])
                    copy_with_symlinks(f"{current_path_location}/Apps/EfazRobloxBootstrapMac/Apps/Play Roblox.app", stored_main_app[found_platform][2])

                    # Prepare Contents of .app files
                    printMainMessage("Preparing Contents..")
                    if os.path.exists(stored_main_app[found_platform][0]):
                        # Add App Icon for Finder to cache
                        printMainMessage("Adding App Icon..")
                        shutil.copy(f"AppIcon.icns", f"{stored_main_app[found_platform][0]}/Icon")
                        shutil.copy(f"AppIcon.icns", f"{stored_main_app[found_platform][1]}/Icon")

                        # Export ./ to /Contents/Resources/
                        printMainMessage("Copying Main Resources..")
                        shutil.copytree(f"{current_path_location}/", f"{stored_main_app[found_platform][1]}/Contents/Resources/", dirs_exist_ok=True, ignore=ignore_files_func, symlinks=True)
                        
                        # Reduce Download Safety Measures
                        # This can prevent messages like: Apple could not verify “EfazRobloxBootstrap.app” is free of malware that may harm your Mac or compromise your privacy.
                        if disable_download_for_app == True:
                            printMainMessage("Reducing Download Safety Measures for Allowing Runtime..")
                            subprocess.run(f"xattr -rd com.apple.quarantine \"/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz's Roblox Bootstrap.app/\"", shell=True, stdout=subprocess.DEVNULL)
                            subprocess.run(f"xattr -rd com.apple.quarantine \"/Applications/EfazRobloxBootstrap.app/Contents/MacOS/Efaz's Roblox Bootstrap.app/\"", shell=True, stdout=subprocess.DEVNULL)

                        # Remove Apps Folder in /Contents/Resources/
                        printMainMessage("Removing Apps Folder in /Contents/Resources/ to save space.")
                        if os.path.exists(os.path.join(stored_main_app[found_platform][0], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][0], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][1], "Contents", "Resources", "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][2], "Contents", "Resources", "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][2], "Contents", "Resources", "Apps"))

                        # Sync FastFlagConfiguration.json files
                        printMainMessage("Copying Configuration Files..")
                        fast_config_path = os.path.join(stored_main_app[found_platform][0], "Contents", "Resources", "FastFlagConfiguration.json")
                        if os.path.exists(fast_config_path):
                            if not ("EfazRobloxBootstrap.app" in current_path_location): fastFlagConfig["EFlagEfazRobloxBootStrapSyncDir"] = current_path_location
                            with open(fast_config_path, "w") as f:
                                json.dump(fastFlagConfig, f, indent=4)
                        else:
                            if not ("EfazRobloxBootstrap.app" in current_path_location): fastFlagConfig["EFlagEfazRobloxBootStrapSyncDir"] = current_path_location
                            with open(fast_config_path, "w") as f:
                                json.dump(fastFlagConfig, f, indent=4)

                        # Success!
                        if overwrited == True:
                            printSuccessMessage(f"Successfully updated Efaz's Roblox Bootstrap!")
                        else:
                            printSuccessMessage(f"Successfully installed Efaz's Roblox Bootstrap!")
                    else:
                        printErrorMessage("Something went wrong trying to find the application folder.")
                    shutil.rmtree(f"{current_path_location}/Apps/EfazRobloxBootstrapMac/")
                else:
                    printErrorMessage("Something went wrong trying to find the installation folder.")
            elif main_os == "Windows":
                if os.path.exists(f"{current_path_location}/Apps/EfazRobloxBootstrapWindows.zip"):
                    # Unzip Installation ZIP
                    printMainMessage("Unzipping Installation ZIP File..")
                    try:
                        subprocess.run(["powershell", "-command", f"Expand-Archive -Path '{current_path_location}/Apps/EfazRobloxBootstrapWindows.zip' -DestinationPath '{current_path_location}/Apps/EfazRobloxBootstrapWindows/' -Force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    except Exception as e:
                        printErrorMessage(f"Something went wrong while trying to unzip macOS apps file: {str(e)}")
                    time.sleep(1)
                else:
                    printYellowMessage("Something went wrong finding EfazRobloxBootstrapWindows.zip. It will require a EfazRobloxBootstrapWindows folder in order for installation to finish.")
                if os.path.exists(f"{current_path_location}/Apps/EfazRobloxBootstrapWindows/"):
                    # Get FastFlagConfiguration.json Data
                    if overwrited == True:
                        printMainMessage("Getting Configuration File Data..")
                        if os.path.exists(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json")):
                            with open(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json"), "r") as f:
                                fastFlagConfig = json.load(f)
                        else:
                            fastFlagConfig = {}
                    else:
                        fastFlagConfig = {}

                    # Delete Other Operating System Files
                    deleted_other_os = False
                    if not (disable_remove_other_operating_systems == True or fastFlagConfig.get("EFlagDisableDeleteOtherOSApps") == True):
                        if os.path.exists(os.path.join(current_path_location, "/Apps/EfazRobloxBootstrapMac.zip")):
                            os.remove(os.path.join(current_path_location, "/Apps/EfazRobloxBootstrapMac.zip"))
                            deleted_other_os = True
                        if deleted_other_os == True: printMainMessage("To help save space, the script has automatically deleted files made for other operating systems!")

                    # Convert All Mod Modes to Mods
                    if os.path.exists(os.path.join(current_path_location, "/ModModes/")):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(os.path.join(current_path_location, "/ModModes/")):
                            mod_mode_path = os.path.join(os.path.join(current_path_location, "/ModModes/"), i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(os.path.join(current_path_location, f"/Mods/{i}/")):
                                    os.makedirs(os.path.join(current_path_location, f"/Mods/{i}/"), exist_ok=True)
                                shutil.copytree(mod_mode_path, f"{current_path_location}/Mods/{i}/", dirs_exist_ok=True)
                        shutil.rmtree(os.path.join(current_path_location, "/ModModes/"))
                    if os.path.exists(os.path.join(stored_main_app[found_platform][0], "ModModes")):
                        printMainMessage("Converting Mod Modes to Mods..")
                        for i in os.listdir(os.path.join(stored_main_app[found_platform][0], "ModModes")):
                            mod_mode_path = os.path.join(os.path.join(stored_main_app[found_platform][0], "ModModes"), i)
                            if os.path.isdir(mod_mode_path):
                                if not os.path.exists(os.path.join(stored_main_app[found_platform][0], "Mods", i)):
                                    os.makedirs(os.path.join(stored_main_app[found_platform][0], "Mods", i), exist_ok=True)
                                shutil.copytree(mod_mode_path, os.path.join(stored_main_app[found_platform][0], "Mods", i), dirs_exist_ok=True)
                        shutil.rmtree(os.path.join(stored_main_app[found_platform][0], "ModModes"))

                    # Copy Apps
                    printMainMessage("Creating paths..")
                    os.makedirs(stored_main_app[found_platform][0], exist_ok=True)
                    printMainMessage("Installing EXE File..")
                    if is_x86_windows() or use_x86_windows == True:
                        shutil.copy(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap32", "EfazRobloxBootstrap32.exe"), stored_main_app[found_platform][1])
                        shutil.copy(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "PlayRoblox32.exe"), os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"))
                        shutil.copytree(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap32", "_internal"), os.path.join(stored_main_app[found_platform][0], "_internal"), dirs_exist_ok=True)
                    else:
                        if os.path.exists(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap", "EfazRobloxBootstrap.exe")):
                            shutil.copy(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap", "EfazRobloxBootstrap.exe"), stored_main_app[found_platform][1])
                            shutil.copy(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows",  "PlayRoblox.exe"), os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"))
                            shutil.copytree(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap", "_internal"), os.path.join(stored_main_app[found_platform][0], "_internal"), dirs_exist_ok=True)
                        else:
                            printErrorMessage("There was an issue trying to find the x64 version of the Windows app. Would you like to install the 32-bit version? [32-bit Python is not needed.]")
                            a = input("> ")
                            if not (a.lower() == "n"):
                                shutil.copy(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap32", "EfazRobloxBootstrap32.exe"), stored_main_app[found_platform][1])
                                shutil.copy(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows",  "PlayRoblox32.exe"), os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"))
                                shutil.copytree(os.path.join(current_path_location, "Apps", "EfazRobloxBootstrapWindows", "EfazRobloxBootstrap32", "_internal"), os.path.join(stored_main_app[found_platform][0], "_internal"), dirs_exist_ok=True)
                            else:
                                sys.exit(0)

                    # Reduce Download Safety Measures
                    # This can prevent messages from Microsoft Smartscreen
                    if disable_download_for_app == True:
                        printMainMessage("Reducing Download Safety Measures for Allowing Runtime..")
                        subprocess.run(["powershell", "-Command", f'Unblock-File -Path "{stored_main_app[found_platform][1]}"'], shell=True, stdout=subprocess.DEVNULL)
                        subprocess.run(["powershell", "-Command", f'Unblock-File -Path "{os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe")}"'], shell=True, stdout=subprocess.DEVNULL)

                    # Setup URL Schemes
                    import winreg
                    if instant_install == False:
                        if not (disabled_url_scheme_installation == True):
                            printMainMessage("Setting up URL Schemes..")
                            def set_url_scheme(protocol, exe_path):
                                protocol_key = r"Software\Classes\{}".format(protocol)
                                command_key = r"Software\Classes\{}\shell\open\command".format(protocol)

                                try:
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, protocol_key) as key:
                                        winreg.SetValue(key, "", winreg.REG_SZ, "URL:{}".format(protocol))
                                        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, protocol)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
                                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"{}" "%1"'.format(exe_path))
                                    printSuccessMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                except Exception as e:
                                    printErrorMessage(f"An error occurred: {e}")
                            set_url_scheme("efaz-bootstrap", stored_main_app[found_platform][1])
                            set_url_scheme("roblox-player", stored_main_app[found_platform][1])
                            set_url_scheme("roblox", stored_main_app[found_platform][1])
                    else:
                        if not (fastFlagConfig.get("EFlagDisableURLSchemeInstall") == True):
                            printMainMessage("Setting up URL Schemes..")
                            def set_url_scheme(protocol, exe_path):
                                protocol_key = r"Software\Classes\{}".format(protocol)
                                command_key = r"Software\Classes\{}\shell\open\command".format(protocol)

                                try:
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, protocol_key) as key:
                                        winreg.SetValue(key, "", winreg.REG_SZ, "URL:{}".format(protocol))
                                        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, protocol)
                                    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_key) as key:
                                        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, '"{}" "%1"'.format(exe_path))
                                    printSuccessMessage(f'URL scheme "{protocol}" has been set for "{exe_path}"')
                                except Exception as e:
                                    printErrorMessage(f"An error occurred: {e}")
                            set_url_scheme("efaz-bootstrap", stored_main_app[found_platform][1])
                            set_url_scheme("roblox-player", stored_main_app[found_platform][1])
                            set_url_scheme("roblox", stored_main_app[found_platform][1])

                    # Setup Shortcuts
                    if not (disabled_shortcuts_installation == True or fastFlagConfig.get("EFlagDisableShortcutsInstall") == True):
                        printMainMessage("Setting up shortcuts..")
                        try:
                            import win32com.client # type: ignore
                            def create_shortcut(target_path, shortcut_path, working_directory=None, icon_path=None):
                                shell = win32com.client.Dispatch('WScript.Shell')
                                shortcut = shell.CreateShortcut(shortcut_path)
                                shortcut.TargetPath = target_path
                                if working_directory:
                                    shortcut.WorkingDirectory = working_directory
                                if icon_path:
                                    shortcut.IconLocation = icon_path
                                shortcut.save()
                            create_shortcut(stored_main_app[found_platform][1], os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Efaz's Roblox Bootstrap.lnk"))
                            create_shortcut(stored_main_app[found_platform][1], os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), "Efaz's Roblox Bootstrap.lnk"))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"), os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 'Play Roblox.lnk'))
                            create_shortcut(os.path.join(stored_main_app[found_platform][2], "PlayRoblox.exe"), os.path.join(os.path.join(os.path.join(os.environ['APPDATA']), 'Microsoft', 'Windows', 'Start Menu', 'Programs'), 'Play Roblox.lnk'))
                        except Exception as e:
                            printYellowMessage(f"There was an issue setting shortcuts and may be caused due to OneDrive. Error: {str(e)}")

                    # Copy App Resources
                    printMainMessage("Copying App Resources..")
                    if os.path.exists(stored_main_app[found_platform][1]):
                        shutil.copytree(current_path_location, stored_main_app[found_platform][0], dirs_exist_ok=True, ignore=ignore_files_func)

                        # Handle Existing Configuration Files
                        printMainMessage("Copying Configuration Files..")
                        if os.path.exists(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json")):
                            if disabled_url_scheme_installation == True:
                                fastFlagConfig["EFlagDisableURLSchemeInstall"] = True
                            elif disabled_url_scheme_installation == False:
                                fastFlagConfig["EFlagDisableURLSchemeInstall"] = False
                            if disabled_shortcuts_installation == True:
                                fastFlagConfig["EFlagDisableShortcutsInstall"] = True
                            elif disabled_shortcuts_installation == False:
                                fastFlagConfig["EFlagDisableShortcutsInstall"] = False

                            if use_installation_syncing == True:
                                if not ("/Local/EfazRobloxBootstrap/" in current_path_location): fastFlagConfig["EFlagEfazRobloxBootStrapSyncDir"] = current_path_location
                            with open(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json"), "w") as f:
                                json.dump(fastFlagConfig, f, indent=4)
                        else:
                            if disabled_url_scheme_installation == True:
                                fastFlagConfig["EFlagDisableURLSchemeInstall"] = True
                            elif disabled_url_scheme_installation == False:
                                fastFlagConfig["EFlagDisableURLSchemeInstall"] = False
                            if disabled_shortcuts_installation == True:
                                fastFlagConfig["EFlagDisableShortcutsInstall"] = True
                            elif disabled_shortcuts_installation == False:
                                fastFlagConfig["EFlagDisableShortcutsInstall"] = False

                            if use_installation_syncing == True:
                                if not ("/Local/EfazRobloxBootstrap/" in current_path_location): fastFlagConfig["EFlagEfazRobloxBootStrapSyncDir"] = current_path_location
                            with open(os.path.join(f"{stored_main_app[found_platform][0]}", "FastFlagConfiguration.json"), "w") as f:
                                json.dump(fastFlagConfig, f, indent=4)

                        # Remove Apps Folder in Installed Folder
                        printMainMessage("Removing Apps Folder in Installed Folder to save space.")
                        if os.path.exists(os.path.join(stored_main_app[found_platform][0], "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][0], "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][1], "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][1], "Apps"))
                        if os.path.exists(os.path.join(stored_main_app[found_platform][2], "Apps")):
                            shutil.rmtree(os.path.join(stored_main_app[found_platform][2], "Apps"))

                        # Mark Installation in Windows
                        printMainMessage("Marking Program Installation into Windows..")
                        app_key = "Software\\EfazRobloxBootstrap"
                        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_key) as key:
                            winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, stored_main_app[found_platform][0])
                            winreg.SetValueEx(key, "Installed", 0, winreg.REG_DWORD, 1)

                        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\EfazRobloxBootstrap"
                        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
                            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f"py {os.path.join(stored_main_app[found_platform][0], "Uninstall.py")}")
                            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Efaz's Roblox Bootstrap")
                            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.2.0")
                            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(stored_main_app[found_platform][0], "AppIcon.ico"))

                        # Success!
                        if overwrited == True:
                            printSuccessMessage(f"Successfully updated Efaz's Roblox Bootstrap!")
                        else:
                            printSuccessMessage(f"Successfully installed Efaz's Roblox Bootstrap!")
                        shutil.rmtree(f"{current_path_location}/Apps/EfazRobloxBootstrapWindows/")
                    else:
                        printErrorMessage("Something went wrong trying to find the installation folder.")
                else:
                    printErrorMessage("Something went wrong trying to find the installation folder.")
            else:
                printErrorMessage("Efaz's Roblox Bootstrap is only supported for macOS and Windows.")
        else:
            printErrorMessage("There was an issue while finding the Apps folder for installation.")
    if silent_mode == True:
        instant_install = True
        try:
            install()
        except Exception as e:
            printErrorMessage(f"Something went wrong during installation: {str(e)}")
    else:
        if overwrited == True:
            printWarnMessage("--- Updater ---")
        else:
            printWarnMessage("--- Installer ---")
        if instant_install == True:
            try:
                install()
            except Exception as e:
                printErrorMessage(f"Something went wrong during installation: {str(e)}")
            if rebuild_mode == False: input("> ")
        else:
            printMainMessage("Welcome to Efaz's Roblox Bootstrap Installer!")
            printMainMessage("Efaz's Roblox Bootstrap is a Roblox bootstrap that allows you to add modifications to your Roblox client using files, activity tracking and Python!")
            printMainMessage("Before we continue to installing, you must complete these questions before you can install!")
            printMainMessage("If you want to say yes, type \"y\". Otherwise, type \"n\". Anyway, here ya go!")

            try:
                import requests
                import plyer
                import pypresence
                if main_os == "Darwin":
                    import posix_ipc
                    import objc
                    import tkinter
                elif main_os == "Windows":
                    import win32com.client # type: ignore
            except Exception as e:
                printMainMessage("Some modules are not installed and may be needed for some features. Do you want to install all the modules needed now? (y/n)")
                if instant_install == True or isYes(input("> ")) == True:
                    pip_class.install(["requests", "plyer", "pypresence"])
                    if main_os == "Darwin":
                        pip_class.install(["posix-ipc", "pyobjc", "tk"])
                    elif main_os == "Windows":
                        pip_class.install(["pywin32"])
                    import requests
                    import plyer
                    import pypresence
                    if main_os == "Darwin":
                        import posix_ipc
                        import objc
                        import tkinter
                    elif main_os == "Windows":
                        import win32com.client # type: ignore
                    printSuccessMessage("Successfully installed modules!")
                else:
                    printErrorMessage("Ending installation..")
                    sys.exit(0)
            
            printMainMessage("Would you like to check for any new bootstrap updates right now? (y/n)")
            a = input("> ")
            if isYes(a) == True:
                try:
                    import requests
                except Exception as e:
                    printMainMessage("Some modules are not installed. Do you want to install all the modules required now? (y/n)")
                    pip_class.install(["requests"])
                    import requests
                    printSuccessMessage("Successfully installed modules!")
                version_server = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/Version.json"
                if not (type(version_server) is str and version_server.startswith("https://")): version_server = "https://raw.githubusercontent.com/EfazDev/roblox-bootstrap/main/Version.json"
                latest_vers_res = requests.get(f"{version_server}")
                if latest_vers_res.ok:
                    latest_vers = latest_vers_res.json()
                    if current_version.get("version"):
                        if current_version.get("version", "1.0.0") < latest_vers.get("latest_version", "1.0.0"):
                            download_location = latest_vers.get("download_location", "https://github.com/EfazDev/roblox-bootstrap/archive/refs/heads/main.zip")
                            printWarnMessage("--- New Bootstrap Update ---")
                            printMainMessage(f"We have detected a new version of Efaz's Roblox Bootstrap! Would you like to install it? (y/n)")
                            if download_location == "https://github.com/EfazDev/roblox-bootstrap/archive/refs/heads/main.zip":
                                printSuccessMessage("✅ This version is a public update available on GitHub for viewing.")
                            elif download_location == "https://cdn.efaz.dev/cdn/py/roblox-bootstrap-beta.zip":
                                printYellowMessage("⚠️ This version is a beta and may cause issues with your installation.")
                            else:
                                printErrorMessage("❌ The download location for this version is different from the official GitHub download link!! You may be downloading an unofficial Efaz's Roblox Bootstrap version!")
                            printSuccessMessage(f"v{current_version.get('version', '1.0.0')} [Current] => v{latest_vers['latest_version']} [Latest]")
                            if isYes(input("> ")) == True:
                                printMainMessage("Downloading latest version..")
                                download_update = subprocess.run(["curl", "-L", download_location, "-o", "./Update.zip"], check=True)
                                if download_update.returncode == 0:
                                    printMainMessage("Download Success! Extracting ZIP now!")
                                    if main_os == "Darwin":
                                        zip_extract = subprocess.run(["unzip", "-o", "Update.zip", "-d", "./Update/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    elif main_os == "Windows":
                                        zip_extract = subprocess.run(["powershell", "-command", f"Expand-Archive -Path 'Update.zip' -DestinationPath './Update/' -Force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                                    if zip_extract.returncode == 0:
                                        printMainMessage("Extracted successfully! Installing Files!")
                                        for file in os.listdir("./Update/roblox-bootstrap-main/"):
                                            src_path = os.path.join("./Update/roblox-bootstrap-main/", file)
                                            dest_path = os.path.join("./", file)
                                            
                                            if os.path.isdir(src_path):
                                                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                                            else:
                                                if not file.endswith(".json"):
                                                    shutil.copy2(src_path, dest_path)
                                        printMainMessage("Cleaning up files..")
                                        os.remove("Update.zip")
                                        shutil.rmtree("./Update/")
                                        printSuccessMessage(f"Update to v{latest_vers['version']} was finished successfully! Restarting installer..")
                                        subprocess.run(args=[sys.executable] + sys.argv)
                                        sys.exit(0)
                                    else:
                                        printMainMessage("Cleaning up files..")
                                        os.remove("Update.zip")
                                        shutil.rmtree("./Update/")
                                        printErrorMessage("Extracting ZIP File failed. Would you like to continue to Roblox without updating? (y/n)")
                                        if isYes(input("> ")) == False: sys.exit(0)
                                else:
                                    printErrorMessage("Downloading ZIP File failed. Would you like to continue to Roblox without updating? (y/n)")
                                    if isYes(input("> ")) == False: sys.exit(0)
                        elif current_version.get("version", "1.0.0") > latest_vers.get("latest_version", "1.0.0"):
                            printSuccessMessage("The bootstrap is a beta version! No updates are needed!")
                        else:
                            printMainMessage("The bootstrap is currently on the latest version! No updates are needed!")
                else:
                    printErrorMessage("There was an issue while checking for updates.")
            
            if overwrited == False:
                if main_os == "Windows":
                    printMainMessage("Would you like to set the URL Schemes for the Roblox Client and the bootstrap? [Needed for Roblox Link Shortcuts and when Roblox updates] (y/n)")
                    a = input("> ")
                    if isYes(a) == False:
                        disabled_url_scheme_installation = True
                    printMainMessage("Would you like to make shortcuts for the bootstrap? [Needed for launching through the Windows Start Menu and Desktop] (y/n)")
                    a = input("> ")
                    if isYes(a) == False:
                        disabled_shortcuts_installation = True
                printMainMessage("In order to allow running for the first time, we're gonna reduce download securities for the app bundle. [This won't affect other apps or downloaded files]")
                printMainMessage("This will not bypass scans by your anti-virus software. It will only allow running by the operating system. (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    disable_download_for_app = False
                printMainMessage("Would you like to allow syncing configurations and mods from this folder to the app? (Only 1 installation folder can be used) (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    use_installation_syncing = False
                printMainMessage("Would you like to delete other operating system versions? (This may save 30MB+ of space) (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    disable_remove_other_operating_systems = True
                if remove_unneeded_messages == False: printMainMessage("Alright now, last question, select carefully!")
                if overwrited == True:
                    printMainMessage("Do you want to update Efaz's Roblox Bootstrap? (This will reupdate all files based on this Installation folder.) (y/n)")
                else:
                    printMainMessage("Do you want to install Efaz's Roblox Bootstrap into your system? (y/n)")
                res = input("> ")
                if isYes(res) == True:
                    if remove_unneeded_messages == False: printMainMessage("Yippieee!!!")
                    try:
                        install()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong during installation: {str(e)}")
                    input("> ")
                else:
                    if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
            else:
                printMainMessage("Would you like to delete other operating system versions? (This may save 30MB+ of space) (y/n)")
                a = input("> ")
                if isYes(a) == False:
                    disable_remove_other_operating_systems = True
                printMainMessage("Do you want to update Efaz's Roblox Bootstrap? (This will reupdate all files based on this Installation folder.) (y/n)")
                res = input("> ")
                if isYes(res) == True:
                    if remove_unneeded_messages == False: printMainMessage("Yippieee!!!")
                    try:
                        install()
                    except Exception as e:
                        printErrorMessage(f"Something went wrong during installation: {str(e)}")
                    input("> ")
                else:
                    if remove_unneeded_messages == False: printMainMessage("Aw, well, better next time! (..maybe)")
    sys.exit(0)
else:
    class EfazRobloxBootstrapNotModule(Exception):
        def __init__(self):            
            super().__init__("Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    class EfazRobloxBootstrapInstallerNotModule(Exception):
        def __init__(self):            
            super().__init__("The installer for Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    class EfazRobloxBootstrapLoaderNotModule(Exception):
        def __init__(self):            
            super().__init__("The loader for Efaz's Roblox Bootstrap is only a runable instance, not a module.")
    raise EfazRobloxBootstrapInstallerNotModule()