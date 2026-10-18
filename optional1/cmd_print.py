'''
prints the word Itransition followed by a newline to standard output. However:
-the string must be fewer than 128 characters long;
-it must use no more than 16 distinct characters;
-it must not contain any letters.
'''
from collections import Counter
import unicodedata

text = ""
for i in range(1114111):
    char = chr(i)
    normalized = unicodedata.normalize("NFKC", char)
    if normalized in "print" and unicodedata.category(char).startswith("L") and char not in "print":
        print(f"{i} -> {char} -> {normalized}")
text += chr(120213) + chr(691) + chr(120154) + chr(8345) + chr(120009)
text += "('"
for c in "Itransition":
    text += f"\\{ord(c):o}"
text += "')"
counter = Counter(text)
print(text)
print(len(text))
print(len(list(counter)))