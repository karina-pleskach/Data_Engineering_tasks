from zipfile import ZipFile
from Crypto.Hash import SHA3_256
from functools import reduce
from local_config import EMAIL

SRC = r"task2\task2.zip"

def calculate_sorting_key(hash):
    return reduce(lambda x, y : x * y, [int(h, 16) + 1  for h in hash])

with ZipFile(SRC, "r") as archive:
    file_hashes = [SHA3_256.new(archive.read(name)).hexdigest().lower() for name in archive.namelist()]

file_hashes.sort(key=calculate_sorting_key)
computation_str = ''.join(file_hashes)
computation_str += EMAIL

result = SHA3_256.new(computation_str.encode()).hexdigest().lower()

print(result)