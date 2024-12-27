import os, dotenv, logging, datetime, platform, subprocess, socket
from pathlib import Path

if platform.system() == "Windows":
    import winwifi

class env:
    @staticmethod
    def load(file: str, setting: str) -> dict:
        """
        Load the value of a setting from a dotenv file.

        Args:
            file (str): The path to the dotenv file.
            setting (str): The key of the setting to load.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains the value of requested key, or a string of the exception that occurred.
        """
        try:
            dotenv.load_dotenv(file)
            value = os.getenv(setting)
            return {'success': True, 'result': value}
        except Exception as e:
            return {'success': False, 'result': str(e)}
    
    @staticmethod
    def write(file: str, setting: str, value: str) -> dict:
        """
        Write a value to a setting in a dotenv file and update the environment variable.

        Args:
            file (str): The path to the dotenv file.
            setting (str): The key of the setting to write.
            value (str): The value to write to the setting.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains the value of set key, or a string of the exception that occurred.
        """
        try:
            dotenv.set_key(file, setting, value)
            os.environ[setting] = value
            return {'success': True, 'result': value}
        except Exception as e:
            return {'success': False, 'result': str(e)}

class files:
    @staticmethod
    def check_exist(file: str) -> dict:
        """
        Check if a file exists.

        Args:
            file (str): The path to the file to check.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains True if file exists, False if the file does not exist, or a string of the exception that occurred.
        """
        try:
            with open(file):
                return {'success': True, 'result': True}
        except FileNotFoundError:
            return {'success': True, 'result': False}
        except Exception as e:
            return {'success': False, 'result': str(e)}
    
    @staticmethod
    def create(file: str) -> dict:
        """
        Create a file and its directories if they do not exist.

        Args:
            file (str): The path to the file to create.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains True if file was created, or a string of the exception that occurred.
        """
        try:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'w') as f:
                pass
            return {'success': True, 'result': True}
        except Exception as e:
            return {'success': False, 'result': str(e)}
    
    @staticmethod
    def remove(file: str) -> dict:
        """
        Remove a file.

        Args:
            file (str): The path to the file to remove.

        Returns:
            dict: Dictionary with keys 'success' and 'result', where 'success' is False if an exception occurs. 'result' contains True if file was removed, False if the file was not found, or a string of the exception that occurred.
        """
        try:
            os.remove(file)
            return {'success': True, 'result': True}
        except FileNotFoundError:
            return {'success': True, 'result': False}
        except Exception as e:
            return {'success': False, 'result': str(e)}

class logs:
    def __init__(self, app_name: str, *args, **kwargs):
        """
        Start a logger for the app you're calling from.

        Args:
            app_name: Used to identify app (or section of app) adding to logfile.
        """
        super().__init__(*args, **kwargs)
        # If the logging env file does not exist, create it. Default to level INFO.
        log_settings = str(Path('Settings/logging.env'))
        x = files.check_exist(log_settings)
        if x['success'] and x['result']:
            print(f"File exists: {log_settings}")
        # If file is not found, create it
        elif x['success'] and not x['result']:
            y = files.create(log_settings)
            # Check if creation was successful
            match y['success']:
                # If file was created, add default settings
                case True: 
                    print(f"File created: {log_settings}")
                    settings = {
                        'LOGGING_LEVEL': 'INFO',
                        'LOGGING_DIR': 'Logs/',
                    }
                    for key, value in settings.items():
                        z = env.write(log_settings, key, value)
                        if z['success']:
                            print(f"Set {key} = {value} in {log_settings}")
                        else:
                            print(f"Couldn't write {key} = {value} in {log_settings}")
                            print(f"{z['result']}")
                case False: 
                    print(f"Error creating file: {y['result']}")
        # If there was an exception, print it (since logs not active yet)
        else:
            print(x['result'])

        # Load logging settings
        load_level = env.load(log_settings, 'LOGGING_LEVEL')
        level = load_level['result']
        self.app_logger = logging.getLogger()
        self.app = app_name
        today = datetime.datetime.now().strftime("%b-%d-%Y")
        log_path = f"Logs/{today}.log"
        
        # If file doesn't exist yet, do it.
        x = files.check_exist(log_path)
        if x['success'] and x['result']:
            print(f"File exists: {log_path}")
        # If file is not found, create it
        elif x['success'] and not x['result']:
            y = files.create(log_path)
            # Check if creation was successful
            match y['success']:
                # If file was created, add default settings
                case True: 
                    print(f"Created {log_path}")
                case False: 
                    print(f"Error creating file: {y['result']}")
        # If there was an exception, print it (since logs not active yet)
        else:
            print(x['result'])

        logging.basicConfig(filename=log_path, format="%(message)s")
        # Convert string to actual logging level
        self.level = level.upper() if level else 'INFO'
        self.app_logger.setLevel(getattr(logging, self.level))
        print(f"Logging level set to: {level}")

    # Set the logging level if it needs to be updated
    def set_level(self, level: str):
        """
        Sets the logging level.

        Args:
            level: Accepts (INFO/DEBUG/ERROR/CRITICAL).
        """
        self.new_level = level.upper()
        self.app_logger.setLevel(getattr(logging, self.new_level))
        print(f"Logging level updated to {self.new_level}")

    # Print to log file INFO message
    def info(self, message: str) -> None:
        """
        Enter to the logfile an INFO entry. Format: DateTime - Appname - INFO: Message.

        Args:
            message: What to send to the log.
        """
        self.app_logger.info(f"{self.app} - INFO: {message}")
    
    # Print to log file DEBUG message
    def debug(self, message: str) -> None:
        """
        Enter to the logfile a DEBUG entry. Format: DateTime - Appname - DEBUG: Message.

        Args:
            message: What to send to the log.
        """
        self.app_logger.debug(f"{self.app} - DEBUG: {message}")

    # Print to log file CRTICAL message
    def critical(self, message: str) -> None:
        """
        Enter to the logfile a CRITICAL entry. Format: DateTime - Appname - CRITICAL: Message.

        Args:
            message: What to send to the log.
        """
        self.app_logger.critical(f"{self.app} - CRITICAL: {message}")

    # Print to log file ERROR message
    def error(self, message: str) -> None:
        """
        Enter to the logfile an ERROR entry. Format: DateTime - Appname - ERROR: Message.

        Args:
            message: What to send to the log.
        """
        self.app_logger.error(f"{self.app} - ERROR: {message}")

class Network:
    @staticmethod
    def check_connection() -> dict:
        """
        Check if device is connected to internet.

        Args:
            None

        Returns:
            dict: Dictionary with keys 'success', 'result' and 'type' where 'success' is False if an exception occurs. 'result' contains True if device is connected to internet, False if it is not, or a string of the exception that occurred. 'Type' contains the network connection media type (if applicable).
        """
        try:
        # Connect to cloudflare to check connectivity
            socket.create_connection(("1.1.1.1", 53), timeout=3)
        except OSError:
            return {'success': True, 'result': False, 'type': ""}
        except Exception as e:
            return {'success': False, 'result': str(e), 'type': ""}
        
        if platform.system() == 'Windows':
            try:
                output = subprocess.check_output("netsh interface show interface", shell=True, text=True)
                for line in output.splitlines():
                    if "Connected" in line:
                        if "Wi-Fi" in line:
                            return {'success': True, 'result': True, 'type': "Wi-Fi"}
                        elif "Ethernet" in line:
                            return {'success': True, 'result': True, 'type': "Ethernet"}
                        else:
                            # How did you get here???
                            return {'success': False, 'result': "Something is horribly wrong.. How are you connected to internet without Wi-Fi or Ethernet?"}
            except subprocess.SubprocessError as e:
                return {'success': False, 'result': str(e), 'type': ""}

        elif platform.system() == "Linux":
            try:
            # Check interfaces on Linux (tested on raspian)
                output = subprocess.check_output("nmcli -t -f TYPE,STATE d", shell=True, text=True)
                for line in output.splitlines():
                    if "connected" in line:
                        if "wifi" in line:
                            return {'success': True, 'result': True, 'type': "Wi-Fi"}
                        elif "ethernet" in line:
                            return {'success': True, 'result': True, 'type': "Ethernet"}
            except subprocess.SubprocessError as e:
                return {'success': False, 'result': str(e), 'type': ""}
            
        elif platform.system() == "Darwin":
            return {'success': True, 'result': True, 'type': "MacOS: operation not supported"}

        return {'success': False, 'result': "Unknown system type"}
    
    @staticmethod
    def search_wifi() -> dict:
        """
        Check available wifi networks.

        Args:
            None

        Returns:
            dict: Dictionary with keys 'success', 'result' where 'success' is False if an exception occurs. 'result' will be an list of available Wi-Fi networks.
        """
        wifi_list = []
        if platform.system() == 'Windows':
            try:
                output = winwifi.WinWiFi.scan()
                for item in output:
                    wifi_list.append(item.ssid)
                cleaned_list = list(set(filter(bool, wifi_list)))
            except Exception as e:
                return {'success': False, 'result': str(e)}
            return {'success': True, 'result': cleaned_list}

        elif platform.system() == "Linux":
            try:
                output = subprocess.check_output("nmcli -t -f SSID dev wifi list", shell=True, text=True)
                for line in output.splitlines():
                    wifi_list.append(str(line))
                # This will remove duplicate SSID's (In case of 2.4 and 5GHz, and any empty values in list)
                cleaned_list = list(set(filter(bool, wifi_list)))
            except Exception as e:
                return {'success': False, 'result': str(e)}
            return {'success': True, 'result': cleaned_list}
            
        elif platform.system() == "Darwin":
            return {'success': True, 'result': True, 'type': "MacOS: operation not supported"}
        return {'success': False, 'result': "Unknown system type"}