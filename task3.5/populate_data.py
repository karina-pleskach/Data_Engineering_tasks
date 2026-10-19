import re
import json
import psycopg2
import time
from local_config import DB_USER
from local_config import DB_PASSWORD

FILE = "task3.5/task1_d.json"
CONNECTION = {
    "host" : "localhost",
    "dbname" : "task3.5",
    "user" : DB_USER,
    "password" : DB_PASSWORD
}

with open(FILE, "r", encoding="utf8") as file:
    json_data = re.sub(':(?P<id>[a-z]*)=>', r'"\g<id>":', file.read())
books = json.loads(json_data)

PAGE = 1000
with psycopg2.connect(**CONNECTION) as connection:
    t = time.time()
    with connection.cursor() as cursor:
        for start in range(0, len(books), PAGE):
            cursor.executemany("INSERT INTO book VALUES (%s, %s, %s, %s, %s, %s, %s)", [tuple(dct.values()) for dct in books[start:start+PAGE]])
    connection.commit()
    print(time.time() - t)
