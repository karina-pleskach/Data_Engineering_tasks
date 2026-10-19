import psycopg2
import csv
import time
from local_config import DB_PASSWORD
from local_config  import DB_USER

N = 100_000

CONNECTION = {
    "host" : "localhost",
    "dbname" : "generate_users",
    "user" : DB_USER,
    "password" : DB_PASSWORD,
}

FILE = "gen_users/data.csv"

with open(FILE, "r", newline="") as file:
    users = list(csv.reader(file))[0:N]

PAGE = 1_000

with psycopg2.connect(**CONNECTION) as conn:
    t = time.time()
    with conn.cursor() as cursor:
        for start in range(0, len(users), PAGE):
            cursor.executemany("INSERT INTO users (name, email, address) VALUES (%s, %s, %s)", users[start:start+PAGE])
    conn.commit()
    print(time.time() - t)