from settings import *
import psycopg2

conn = psycopg2.connect(
    f"dbname = {db_name} user = {user_name} password = {password}"
)

conn = psycopg2.connect(
    host=ip,
    database=db_name,
    user=user_name,
    password=password)

cursor = conn.cursor()
cursor.execute("Select * from market")

for row in cursor:
    print(*row, sep='|')
