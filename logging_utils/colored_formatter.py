import logging
import time


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[38;5;244m',  # Grey
        'INFO': '\033[38;5;57m',   # Blue
        'WARNING': '\033[38;5;220m',  # Yellow
        'ERROR': '\033[38;5;160m',  # Red
        'CRITICAL': '\033[38;5;52m',  # Dark-Red
        'TIME': '\033[38;5;40m'
    }
    RESET_CODE = '\033[0m'

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = time.strftime(self.DEFAULT_TIME_FORMAT, ct)
        msecs = str(int(record.msecs))
        return f"{s}.{msecs}"

    def format(self, record):
        name = record.name
        message = record.getMessage()
        log_level = record.levelname
        log_level_color_code = self.COLOR_CODES.get(log_level, self.RESET_CODE)
        time_color_code = self.COLOR_CODES.get('TIME', self.RESET_CODE)

        formatted_time = self.formatTime(record, '%Y-%m-%d %H:%M:%S')
        return f"{time_color_code}[{formatted_time}]{self.RESET_CODE} [{name}] {log_level_color_code}[{log_level}]{self.RESET_CODE}: {message}"
