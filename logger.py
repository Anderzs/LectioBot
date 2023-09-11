import logging
import os
from enum import Enum
from colorama import Fore, Style
from datetime import datetime

class LogLevel(Enum):
    bold = "\033[1m"
    end_bold = "\033[0m"

    WARNING = Fore.YELLOW + bold + "[ADVARSEL]" + end_bold + Fore.RESET
    ERROR = Fore.RED + bold + "[FEJL]" + end_bold + Fore.RESET
    CRITICAL = Fore.RED + bold + "[KRITISK]" + end_bold + Fore.RESET
    INFO = Fore.CYAN + bold + "[INFORMATION]" + end_bold + Fore.RESET
    SUCCES = Fore.GREEN + bold + "[SUCCES]" + end_bold + Fore.RESET


class LogHandler:
    def __init__(self, log_file: str = r"logs/bot.log") -> None:
        self.file_name = log_file.split(".")[0] + "_" + datetime.now().strftime("%d-%m-%Y") + ".log"

        # Opret filen, hvis den ikke allerede eksisterer for dagen
        if not os.path.exists(rf"{self.file_name}"):
            open(self.file_name, "x")

        logging.basicConfig(
            filename=self.file_name,
            format='[%(levelname)-8s] (%(asctime)s): %(message)s',
            filemode='a')
        
        self.log_file = log_file
        self.logger = logging.getLogger()

    def log(self, level: LogLevel, message: str) -> None:
        msg = f"{level.value} | {message}"
        print(msg)

        match level:
            case LogLevel.WARNING:
                self.logger.setLevel(logging.WARNING)
                self.logger.warning(message)
            case LogLevel.ERROR:
                self.logger.setLevel(logging.ERROR)
                self.logger.error(message)
            case LogLevel.CRITICAL:
                self.logger.setLevel(logging.CRITICAL)
                self.logger.critical(message)
            case LogLevel.INFO | LogLevel.SUCCES:
                self.logger.setLevel(logging.INFO)
                self.logger.info(message)
            case _:
                pass