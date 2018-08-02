from instance.database import CursorFromConnectionFromPool, Database


class Ride:
    def __init__(self, starting_point, destination, date, time, available, ride_id):
        self.starting_point = starting_point
        self.destination = destination
        self.date = date
        self.time = time
        self.available = available
        self.ride_id = ride_id

    def __repr__(self):
        return "<Ride: {}>".format(self.starting_point,
                                   self.destination, self.date,
                                   self.time, self.available, self.ride_id)

    def create_ride(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO rides (starting_point, destination, date, time,available)\
                           VALUES (%s ,%s ,%s , %s, %s)"
                           , (self.starting_point,
                              self.destination, self.date,
                              self.time, self.available))

    @staticmethod
    def get_all_rides():
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM rides")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    return rows
            return "Ride not available"

    @classmethod
    def get_ride_by_id(cls, ride_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("select * from rides where ride_id=%s", (ride_id,))
            ride_data = cursor.fetchone()
            if ride_data:
                return ride_data
            return "Ride Doesn't exist"

    @staticmethod
    def delete_ride(ride_id):
        with CursorFromConnectionFromPool() as cursor:
                cursor.execute("DELETE from rides WHERE ride_id=%s ", (ride_id,))

    @staticmethod
    def update_ride(field,new_data,clause,old):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE rides SET %s == %s where %s = "(field,new_data,clause,old))


Database.initialize()
# ride=Ride("nairobi","kiambu","21/02/2018","10:00","True",None)
# ride.create_ride()
my_ride = Ride.update_ride('ride_id',5,'ride_id',7)
# # my_ride=Ride.get_ride_by_id(1)
# my_ride=Ride.delete_ride(8)
# print(my_ride)
