from ride_my_way.api.database import CursorFromConnectionfromPool


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
        with CursorFromConnectionfromPool() as cursor:
            # opens up the connection and automatically commit and close the connection

            # creates cursor using the connection above, with is openning up the cursor
            cursor.execute('INSERT INTO users (email,password,first_name,last_name) VALUES (%s, %s, %s, %s)',
                           (self.email, self.password, self.first_name, self.last_name))

    @classmethod
    def load_from_db_by_email(cls, email):
        with CursorFromConnectionfromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
            user_data = cursor.fetchone()
            return cls(email=user_data[0], password=user_data[1], first_name=user_data[2], last_name=user_data[3],
                       _id=user_data[4])
