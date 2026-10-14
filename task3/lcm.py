import math

def count_lcm(x, y):
    if not is_natural_number(x, y):
        return "NaN"
    return str(math.lcm(int(x), int(y)))

def is_natural_number(*strs):
    digits_characters = "0123456789"
    if not all(strs): return False
    return all(s in digits_characters for str in strs for s in str)