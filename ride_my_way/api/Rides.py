from instance.database import CursorFromConnectionFromPool, Database


class Ride:
    def __init__(self,  starting_point, destination, date, time,available,ride_id):
        self.starting_point = starting_point
        self.destination = destination
        self.date = date
        self.time = time
        self.available=available
        self.ride_id = ride_id

    def __repr__(self):
        return "<Ride: {}>".format(self.starting_point,
                                   self.destination, self.date,
                                   self.time,self.available,self.ride_id )

    def create_ride(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("INSERT INTO rides (starting_point, destination, date, time,available,ride_id)\
                           VALUES (%s ,%s ,%s , %s, %s, %s)"
                           , ( self.starting_point,
                              self.destination, self.date,
                              self.time,self.available,self.ride_id))

    @classmethod
    def get_all_rides(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("SELECT * FROM rides")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    return rows,"/n"
            return "no such a ride"

Database.initialize()
ride=Ride("nairobi","kiambu","21/02/2018","10:00","True",None)
ride.create_ride()
my_ride=Ride.get_all_rides()
print(my_ride)