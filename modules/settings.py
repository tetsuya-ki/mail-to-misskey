import os
from os.path import join, dirname
from dotenv import load_dotenv
from logging import DEBUG, INFO, WARN, ERROR

def if_env(str):
    if str is None or str.upper() != 'TRUE':
        return False
    else:
        return True

def if_env_defalut_true(str):
    if str is None or str.upper() == 'TRUE':
        return True
    else:
        return False

def get_log_level(str):
    if str is None:
        return WARN
    upper_str = str.upper()
    if upper_str == 'DEBUG':
        return DEBUG
    elif upper_str == 'INFO':
        return INFO
    elif upper_str == 'ERROR':
        return ERROR
    else:
        return WARN

def num_env(param):
    if str is None or not str(param).isdecimal():
        return 5
    else:
        return int(param)


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), 'files' + os.sep + '.env')
load_dotenv(dotenv_path)


MISSKEY_POST_URL = os.environ.get('MISSKEY_POST_URL')
MISSKEY_TOKEN = os.environ.get('MISSKEY_TOKEN')
LOG_LEVEL = get_log_level(os.environ.get('LOG_LEVEL'))
HASHTAG = get_log_level(os.environ.get('HASHTAG'))
TARGET_SUBJECT = get_log_level(os.environ.get('TARGET_SUBJECT'))
MAIL_POP3_SERVER = os.environ.get('MAIL_POP3_SERVER')
MAIL_POP3_PORT = os.environ.get('MAIL_POP3_PORT')
MAIL_USER = os.environ.get('MAIL_USER')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')