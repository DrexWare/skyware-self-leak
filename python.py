import os
import pyfiglet
import colorama
import fade
import requests
import random
import string
import subprocess
import sys
import threading
import json

processes = [
        "epicgameslauncher.exe",
        "EpicWebHelper.exe",
        "FortniteClient-Win64-Shipping_EAC.exe",
        "FortniteClient-Win64-Shipping_BE.exe",
        "FortniteLauncher.exe",
        "FortniteClient-Win64-Shipping.exe",
        "EpicGamesLauncher.exe",
        "EasyAntiCheat.exe",
        "BEService.exe",
        "BEServices.exe",
        "BattleEye.exe"
    ]

# Initialize colorama
colorama.init(autoreset=True)

# Define colors
RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
RESET = colorama.Fore.RESET

def clear_console():
    """Clear the console based on the operating system."""
    os.system("cls" if os.name == "nt" else "clear")

def log(message, errlvl=0):
    """Log messages with different severity levels."""
    if errlvl == 0:
        print(f"{BLUE}[-] {message}{RESET}")
    elif errlvl == 1:
        print(f"{RED}[!] {message}{RESET}")
    elif errlvl == 2:
        print(f"{YELLOW}[?] {message}{RESET}")

def logo():
    """Display the logo and title of the application."""
    clear_console()
    logoFade = fade.greenblue(pyfiglet.figlet_format("D r e x w a r e", font="big"))
    print(logoFade)
    print("Spoofer v1".center(65, "="))
    print(f"{YELLOW}Drexware temp - Made By Drexxy - drexxware.gg{RESET}".center(65))

def download_file(url, directory):
    """Download a file from a URL to a specified directory."""
    filename = os.path.basename(url)
    file_path = os.path.join(directory, filename)

    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directory if it doesn't exist
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return file_path  # Return the file path for later use
    
    except requests.exceptions.RequestException as e:
        log(f"Download failed: {e}", errlvl=1)
        return None

def generate_random_filename(extension):
    """Generate a random filename with a given extension."""
    random_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 9)))
    return f"{random_name}{extension}"

def validate_key(pastebin_url, key):
    """Validate the provided key against a Pastebin entry."""
    try:
        response = requests.get(pastebin_url)
        response.raise_for_status()
        keys_data = json.loads(response.text)

        for entry in keys_data:
            if entry['Key'] == key:
                if entry['ExpirationDate'] > "2023-11-01T00:00:00Z":  # Check expiration date
                    return True
                else:
                    log("Key has expired.", 1)
                    return False
        
        log("Key not found.", 1)
        return False

    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch keys: {e}", 1)
        return False
    except json.JSONDecodeError:
        log("Failed to decode JSON from Pastebin.", 1)
        return False

def run_in_background(command, cleanup_files):
    """Run a command in the background and capture its output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def read_output():
        """Read the output and error streams and log them."""
        for line in iter(process.stdout.readline, ''):
            log(line.strip())
        process.stdout.close()
        
        # Wait for the process to finish and capture errors
        process.wait()
        if process.returncode != 0:
            error_output = process.stderr.read()
            log(error_output.strip(), errlvl=1)

        # Cleanup files after execution
        for file in cleanup_files:
            if os.path.exists(file):
                os.remove(file)

    # Start a thread to read output
    threading.Thread(target=read_output, daemon=True).start()
def run_commands(command_string):
    # Split the command string into individual commands
    commands = command_string.split(';')
    
    for command in commands:
        command = command.strip()  # Remove leading/trailing whitespace
        if command:  # Check if the command is not empty
            try:
                print(f"Running command: {command}")
                # Execute the command
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                print(result.stdout)  # Print the output of the command
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while executing '{command}': {e.stderr}")

def task_kill(processes):
    killed_count = 0
    for process in processes:
        command = f'taskkill /f /im {process} > nul 2>&1'
        result = os.system(command)
        if result == 0:
            killed_count += 1


def perform_regedit_clean():
    registry_keys = [
        r"HKLM\SYSTEM\ControlSet001\Services\EpicOnlineServices",
        r"HKCU\SOFTWARE\Epic Games",
        r"HKLM\SOFTWARE\Classes\com.epicgames.launcher",
        r"HKLM\SYSTEM\ControlSet001\Services\BEService",
        r"HKLM\SYSTEM\ControlSet001\Services\BEDaisy",
        r"HKLM\SYSTEM\ControlSet001\Services\EasyAntiCheat",
        r"HKLM\SYSTEM\CurrentControlSet\Services\BEService",
        r"HKLM\SYSTEM\CurrentControlSet\Services\BEDaisy",
        r"HKLM\SYSTEM\CurrentControlSet\Services\EasyAntiCheat",
        r"HKLM\SOFTWARE\WOW6432Node\EasyAntiCheat",
        r"HKLM\SOFTWARE\WOW6432Node\Epic Games",
        r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\microphone\NonPackaged",
        r"HKLM\SOFTWARE\Microsoft\RADAR\HeapLeakDetection\DiagnosedApplications",
        r"HKCU\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\com.epicgames.launcher",
        r"HKCR\com.epicgames.eos",
        r"HKLM\SOFTWARE\EpicGames",
        r"HKEY_USERS\S-1-5-18\Software\Epic Games",
        r"HKCU\SOFTWARE\Epic Games\Fortnite",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\GameSettings",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Launcher",
        r"HKLM\SOFTWARE\Epic Games\Fortnite",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\GameSettings",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Launcher",
        r"HKLM\SYSTEM\CurrentControlSet\Services\FortniteService",
        r"HKLM\SYSTEM\CurrentControlSet\Services\FortniteLauncher",
        r"HKCU\SOFTWARE\Epic Games\Launcher",
        r"HKLM\SOFTWARE\Epic Games\Launcher",
        r"HKLM\SOFTWARE\WOW6432Node\EpicGames",
        r"HKLM\SYSTEM\ControlSet001\Services\EpicGamesLauncher",
        r"HKLM\SYSTEM\CurrentControlSet\Services\EpicGamesLauncher",
        r"HKLM\SOFTWARE\EpicGames\Fortnite\InstallLocation",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\PlayerPrefs",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Accounts",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Settings",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\PlayerPrefs",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Accounts",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Settings",
        r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Epic Games",
        r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Epic Games",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Update",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\InstallLocation",
        r"HKLM\SYSTEM\ControlSet001\Services\FortniteClient",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Friends",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Friends",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Achievements",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Achievements",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\VoiceSettings",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\VoiceSettings",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Matchmaking",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Matchmaking",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\CloudSaves",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\CloudSaves",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Analytics",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Analytics",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Localization",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Localization",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Reports",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Configuration",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Configuration",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\ErrorLogs",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\ErrorLogs",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\GameHistory",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\GameHistory",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\GameInstallations",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\GameInstallations",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Notifications",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Notifications",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\ParentalControls",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\ParentalControls",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Social",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Social",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\SeasonPass",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\SeasonPass",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Skins",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Skins",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\SeasonStats",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\SeasonStats",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\RecentMatches",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\RecentMatches",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Inventory",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Inventory",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\BattlePass",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\BattlePass",
        r"HKCU\SOFTWARE\Epic Games\Fortnite\Events",
        r"HKLM\SOFTWARE\Epic Games\Fortnite\Events"
    ]
    
    for key in registry_keys:
        os.system(f'reg delete "{key}" /f > nul 2>&1')


def perform_deep_directories_clean():
    deep_clean_dirs = [
        r"%systemdrive%\Users\%username%\AppData\Local\Microsoft\Windows\INetCookies",
        r"%systemdrive%\Users\%username%\AppData\Local\Microsoft\Windows\History",
        r"%systemdrive%\Users\%username%\AppData\Local\Microsoft\Windows\INetCache",
        r"%systemdrive%\Users\%username%\AppData\Local\Temp",
        r"%systemdrive%\Windows\Temp",
        r"%systemdrive%\Windows\Prefetch",
        r"%systemdrive%\Temp",
        r"%systemdrive%\*.etl",
        r"%systemdrive%\*.log",
        r"%systemdrive%\*.tmp",
        r"%systemdrive%\*.old",
        r"%systemdrive%\*.bak",
        r"%systemdrive%\*.bac",
        r"%systemdrive%\*.bup",
        r"%systemdrive%\*.chk",
        r"%systemdrive%\*.dmp",
        r"%systemdrive%\*.temp",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite",
        r"%systemdrive%\Users\%username%\Documents\My Games\Fortnite",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games",
        r"%systemdrive%\Users\%username%\AppData\Local\Fortnite",
        r"%systemdrive%\Users\%username%\AppData\Roaming\Epic Games",
        r"%systemdrive%\Users\%username%\AppData\Local\FortniteGame",
        r"%systemdrive%\Users\%username%\AppData\Local\FortniteLauncher",
        r"%systemdrive%\Users\%username%\Saved Games\Epic Games\Fortnite",
        r"%systemdrive%\Users\%username%\AppData\Local\FortniteGame\Saved",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Launcher",
        r"%systemdrive%\Users\%username%\AppData\Local\Temp\FortniteTemp",
        r"%systemdrive%\Users\%username%\Documents\Epic Games\Fortnite",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Temp",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Logs",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Screenshots",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Saved",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Backup",
        r"%systemdrive%\Users\%username%\Documents\Fortnite",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Patch",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Updates",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Temp\OldFiles",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Assets",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Maps",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Audio",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Video",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\UI",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Updates",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Assets\Textures",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Assets\Models",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Assets\Sounds",
        r"%systemdrive%\Users\%username%\AppData\Local\Epic Games\Fortnite\Assets\Maps"
    ]
    
    for directory in deep_clean_dirs:
        os.system(f'del /f /s /q "{directory}" > nul 2>&1')


   

    

def main():
    logo()
    log("lasted updated on 11/1/24")
    log("Created by drexxy", 2)
    
    pastebin_url = 'https://pastebin.com/raw/gYcyKfNw'  # Replace with your actual Pastebin URL
    key = input("Enter your key: ")

    if not validate_key(pastebin_url, key):
        log("Invalid key. Exiting...", 1)
        return

    log("Initializing files...")
    
    install_path = "C:\\Windows\\IME\\en-US"
    _mapper = os.path.join(install_path, generate_random_filename('.exe'))
    _driver = os.path.join(install_path, generate_random_filename('.sys'))
    
    map_file_path = download_file("https://github.com/MmCopyMemory/temp-spoof/releases/download/ud/map.exe", _mapper)
    if map_file_path:
        log("Successfully initialized 1/2 files")
    else:
        raise Exception("Make sure antivirus is off and you are connected to the internet")

    driver_file_path = download_file("https://github.com/MmCopyMemory/temp-spoof/releases/download/ud/temp.sys", _driver)
    if driver_file_path:
        log("Successfully initialized 2/2 files")
    else:
        raise Exception("Make sure antivirus is off and you are connected to the internet")

    task_kill(processes)
    command = [map_file_path, driver_file_path]
    run_in_background(command, [map_file_path, driver_file_path])
    
    os.system("pause")
    log("Successfully spoofed!")
    log("Cleaning!")
    
    
    os.system("netsh advfirewall reset > nul 2>&1")
    perform_regedit_clean()
    perform_deep_directories_clean()


if __name__ == "__main__":
    main()
