from collections import defaultdict
import time

def calc_diff(str1, str2):
    diff = 0
    if len(str1) < len(str2):
        temp = str1
        str1 = str2
        str2 = temp
    for i1 in range(len(str1)):
        diff += abs(ord(str1[i1])-(ord(str2[i1]) if i1 < len(str2) else 0))
    return diff

start_time = time.time()
surnames_dict = defaultdict(int)
with open(r'optional2_data\in - Copy.txt', 'r') as file:
    surnames_list = [surname.strip() for surname in file]
for i in range(len(surnames_list)):
    for j in range(i+1, len(surnames_list)):
        diff = calc_diff(surnames_list[i], surnames_list[j])
        surnames_dict[surnames_list[i]] += diff
        surnames_dict[surnames_list[j]] += diff
print(max(surnames_dict, key = surnames_dict.get))
print(f"--- {(time.time() - start_time)} seconds ---")