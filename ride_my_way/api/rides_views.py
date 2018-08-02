'''import dependancies'''
import datetime
from flask import jsonify, Blueprint, request, make_response, session
from ride_my_way import app
from ride_my_way.api.models import Validate
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from ride_my_way.api.Rides import Ride

blacklist = set()

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''Check if token is blacklisted'''
    token_identifier = decrypted_token['jti']
    return token_identifier in blacklist


rides = Blueprint('rides', __name__)
ride_my_way = Validate()


@app.route('/api/v1/rides/<int:id>', methods=['PUT'])
def edit_rides(id):
    '''Function for editing ride info'''
    ride = [ride for ride in ride_my_way.rides_list if ride['ride_id'] == id]
    if len(ride) == 0:
        return jsonify({'message': "Ride Doesn't Exist"}), 404
    if not request.json:
        return jsonify({'message': "No data entered"}), 204
    '''Check if starting point is valid'''
    if 'starting_point' in request.json:
        if ride_my_way.add_ride_validation({'starting_point': request.json['starting_point']}):
            ride[0]['starting_point'] = request.json['starting_point']
        else:
            return jsonify(
                {'message': 'Please enter valid details'})

    '''check if destination is entered and if it is correct'''
    if 'destination' in request.json:
        if ride_my_way.add_ride_validation({'destination': request.json['destination']}):
            ride[0]['destination'] = request.json['destination']
        else:
            return jsonify(
                {'message': 'Please enter a correct destination above 4 characters'})

    '''check if date is correctly entered'''
    if 'time' in request.json:
        if ride_my_way.time_validate(request.json['time']):
            ride[0]['time'] = request.json['time']
        else:
            return jsonify(
                {'message': 'Please enter a correct date format HH:MM'})

    if 'date' in request.json:
        if ride_my_way.date_validate(request.json['date']):
            ride[0]['date'] = request.json['date']
        else:
            return jsonify(
                {'message': 'Please enter a correct date format DD-MM-YYYY'})

        if ride_my_way.add_ride_validation(ride[0]):
            return jsonify({"ride": ride[0]})
    else:
        return jsonify({"message": "please enter valid ride details"})


@app.route('/api/v1/rides', methods=['POST'])
def add_ride():
    '''Function to add a ride'''
    sent_data = request.get_json(force=True)
    data = {

        'starting_point': sent_data.get('starting_point'),
        'destination': sent_data.get('destination'),
        'date': sent_data.get('date'),
        'time': sent_data.get('time'),
        'available':True,
        'ride_id': len(Ride.get_all_rides())+1

    }
    if ride_my_way.add_ride_validation(data) \
            and ride_my_way.date_validate(data['date']) \
            and ride_my_way.time_validate(data['time']):

        ride = Ride(data['starting_point'], data['destination'],
                    data['date'], data['time'], data['available'],None)
        ride.create_ride()
        response = jsonify({
            'ride_id': data['ride_id'],
            'starting_point': data['starting_point'],
            'destination': data['destination'],
            'date': data['date'],
            'time': data['time'],
            'available': True
        })

        response.status_code = 201
        return response
    else:
        return jsonify({"message": "Please enter correct ride details"})


# check if users is correct
@app.route('/api/v1/users/rides/<int:id>', methods=['POST', 'GET', 'PUT'])
@jwt_required
def request_ride(id):
    '''function to retrieve current date'''
    now = datetime.datetime.now()
    email = get_jwt_identity()
    ride = [ride for ride in ride_my_way.rides_list if ride['ride_id'] == id]
    # add data to dictionary
    sent_data = request.get_json(force=True)
    data = {
        'ride_id': id,
        'user_email': email,
        'request_date': now.strftime("%d/%m/%Y"),
        'time': sent_data.get('time')
    }

    if len(ride) == 0:
        return jsonify({'message': "Ride Doesnt Exist"}), 404
    # elif ride[0]['available'] == False:
    #     return jsonify({'message': "The ride has already been borrowed"})
    else:
        ride[0]['available'] = False
        Validate().request_ride(data)
        response = jsonify({
            'ride_id': data['ride_id'],
            'user': data['user_email'],
            'request_date': data['request_date'],
            'time': data['time']
        })
        response.status_code = 201
        return response


@app.route('/api/v1/rides/<int:id>', methods=['DELETE'])
def delete_rides(id):
    '''function to delete ride'''
    ride = Ride.get_ride_by_id(id)
    if ride[4] == id:
        Ride.delete_ride(id)
        return "Ride deleted successfully"
    return "Ride Doesn't exist"

@app.route('/api/v1/rides', methods=['GET'])
def get_all_rides():
    '''function to get all rides'''
    return Ride.get_all_rides(), 200


@app.route('/api/v1/rides/<int:id>', methods=['GET'])
def get_by_id(id):
    '''function to get a single ride by its id'''
    ride = Ride.get_ride_by_id(id)
    if len(ride) == 0:
        return jsonify({'message': "ride Doesnt Exist"}), 404
    return jsonify({'ride': ride}), 200
