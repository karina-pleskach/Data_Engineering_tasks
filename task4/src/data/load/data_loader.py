from pathlib import Path
import config
from src.data.load.file_reader import read
from src.data.load.path_builder import get_store_file_path

def load_data(store_num):
    return {Path(name).stem : read(get_store_file_path(store_num, name)) for name in config.FILE_NAMES}
