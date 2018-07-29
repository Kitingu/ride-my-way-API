# import psycopg2
#
# def add_user():
#     user=User("kasee","asdf","bendeh@gmail.com")
#     User.create_user(user)
# class User:
#     def __init__(self,name,password,email):
#         self.name=name
#         self.password=password
#         self.email=email
#
#     def create_user(self):
#         connection=psycopg2.connect(user="ben",password="asdf",host="localhost",database="rides")
#         cursor=connection.cursor
#         cursor.execute("INSERT INTO user1 (name,password,email)VALUES (?,?,?) )",(self.name,self.password,self.email))
#
# user=User("kasee","asdf","bendeh@gmail.com")
# user.create_user()
from ride_my_way.api.user import User
from ride_my_way.api.database import Database
Database.initialise()

my_user = User.load_from_db_by_email('bendeh@gmail.com')
print(my_user)







