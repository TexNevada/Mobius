import logging
import configparser
import datetime
config = configparser.ConfigParser()
config.read("./config.ini")


def get_log(name: str):
    logger = logging.Logger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(name)s: %(message)s')
    stream_formatter = logging.Formatter('%(message)s')

    if config["Logging"]["logs"].lower() == "true":
        now = datetime.datetime.now()
        time = now.strftime("%d.%m.%y")
        log_file = config["Logging"]["Log_location"]
        file_handler = logging.FileHandler(f"{log_file}/runtime_{time}.log", encoding="utf-8", mode='w')
        file_handler.setLevel(int(config["Logging"]["file_log_Type"]))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    logger.setLevel(int(config["Logging"]["console_log_type"]))
    logger.addHandler(stream_handler)
    return logger
