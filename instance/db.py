import psycopg2

class Database:
    def __init__(self):
        ...

conn = psycopg2.connect(user='ben',
                        password='asdf',
                        database='rides',
                        host='localhost')
cur = conn.cursor()

"""inserting onto the database"""
cur.execute("insert into users (email,first_name,last_name,password) \
            values('kasee@gmail.com','essie','shqo','asdf')")
conn.commit()
"""deleting from the database"""
# cur.execute('delete  from users')
# cur.execute('delete  from users where id=2')

"""updating fields in the database"""
cur.execute("update users set last_name='wanjiku'  where _id = 6")
conn.commit()

"""getting data from the database"""
cur.execute('select * from users ')
rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()
