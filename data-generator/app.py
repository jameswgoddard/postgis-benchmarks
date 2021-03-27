import os, psycopg2, random

db_password = open(os.environ['POSTGRES_PASSWORD_FILE']).read() 
db_user = 'postgres'
db_name = os.environ['POSTGRES_DB']

conn = psycopg2.connect(f"dbname={db_name} user={db_user} password={db_password} host=db")
print(conn)