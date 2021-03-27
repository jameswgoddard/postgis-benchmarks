import os, psycopg2, random, time

# DB login info
db_user = 'postgres'
db_password = open(os.environ['POSTGRES_PASSWORD_FILE']).read() 
db_name = os.environ['POSTGRES_DB']

times = {}

# times format => {'metric_type':[start_time, end_time]}
def print_times():
    for k in times.keys():
        print(f'{k}: {times[k][1] - times[k][0]}')

try:
    # Connect to database container
    conn = psycopg2.connect(f"dbname={db_name} user={db_user} password={db_password} host=db")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute('''CREATE TABLE test 
        (id serial PRIMARY KEY, 
        num integer, 
        data varchar);
    ''')

    # Not sure which is more disruptive, creating all the test data in memory or calling random.sample inline
    times['load'] = [time.time()]
    for i in range(10000):
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

    # Make the changes to the database persistent
    # Should commit be here or further down? 
    # Should commit be measured separately?
    times['load'].append(time.time())
    times['commit'] = [time.time()]
    conn.commit()
    times['commit'].append(time.time())

    # Query the database and measure query time. 
    # Note: the ORM is also taking some time to convert the data to Python objects
    times['query'] = [time.time()]
    cur.execute("SELECT * FROM test LIMIT 1000;")
    times['query'].append(time.time())
    
    # Fetch time will be worth measuring separately when the DB is remote
    # for now this value will be small 
    times['fetch'] = [time.time()]
    result = cur.fetchall()
    times['fetch'].append(time.time())
    #print('load time: %s'%(end_load - start_load), 'query time: %s'%(end_query - start_query), 'fetch time: %s'%(end_fetch - start_fetch))
    print_times()
    # Close communication with the database
    cur.close()
    conn.close()

# If the DB can't be reached then skip most of the logic
# but still raise the error so the container will be restarted
except(psycopg2.OperationalError):
    raise psycopg2.OperationalError