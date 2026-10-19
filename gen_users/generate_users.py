from faker import Faker
import sys
import csv

fake = Faker()
Faker.seed(0)

FILE = 'gen_users/data.csv'
N = 200_000
users = [(
    fake.name(),
    fake.ascii_company_email(),
    fake.address()
    ) for _ in range(N)]

with open(FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(users)
