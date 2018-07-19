from ride_my_way.api.user import User
from ride_my_way.api.database import Database
Database.initialise()

my_user = User.load_from_db_by_email('bendeh@gmail.com')
print(my_user)
