from instance.database import CursorFromConnectionFromPool,Database



class User:
    def __init__(self, email, password, first_name, last_name, _id):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.id = _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO users (email,first_name,last_name,password) \
                            VALUES (%s, %s, %s, %s)", (self.email, self.first_name,
                                                       self.last_name, self.password))

    @classmethod  # this is the currently bound class
    def load_from_db_by_email(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from users WHERE email=%s", (email,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(email=user_data[0], first_name=user_data[1],
                           last_name=user_data[2], password=user_data[3],
                           _id=user_data[4])
            return "user with email {} not found".format(email)

    @classmethod
    def find_by_id(cls, _id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM users WHERE _id = %s", (_id,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(email=user_data[0], first_name=user_data[1],
                           last_name=user_data[2], password=user_data[3],
                           _id=user_data[4])
            return "user not found"
    @classmethod
    def get_all_users(cls):
        with CursorFromConnectionFromPool as cursor:
            cursor.execute("SELECT * FROM users")
    @classmethod  # this is the currently bound class
    def delete_from_dbl(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("DELETE from users where email=%s", (email,))

    @classmethod
    def change_password(cls,user_id,new_pass):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE users SET password= %s WHERE id=%s"(user_id,new_pass))
Database.initialize()
# my_user = User('asdf@gmail.com', 'benjo', 'qwerty', 'asdf', None)
# my_user.save_to_db()
# User.delete_from_dbl("asdf@gmail.com")
# my_user = User.load_from_db_by_email("asdf@gmail.com")
# other_user = User.find_by_id(34)
# print(other_user)
# print(my_user)
