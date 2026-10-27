import config

def get_store_file_path(store_num, file_name):
    return config.DATA_DIR / config.STORE_NAME_TEMPLATE.format(store_num=store_num) / file_name
