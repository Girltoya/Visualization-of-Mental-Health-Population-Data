# key value for different variable
KEY_MAP = 'map'
KEY_DATASET_IAPT = 'dataset_iapt'
KEY_DATASET_CYPED = 'dataset_cyped'
KEY_DATASET_PHSMI = 'dataset_phsmi'
KEY_DATASET_OAPS = 'dataset_oaps'
KEY_CCG_CODE = 'ccg_code'
KEY_MAIN_WINDOW = 'main_window'


def _init():
    """
    init global dictionary to record global variable
    :return: none
    """
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """
    set global variable
    :param key: key
    :param value: value
    :return: none
    """
    _global_dict[key] = value


def get_value(key):
    """
    get global variable
    :param key: key
    :return: global variable
    """
    return _global_dict[key]


