'''import dependancies'''
import unittest
from flask import json
from ride_my_way import app
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))


class TestRides(unittest.TestCase):
    '''Set up methods for test cases'''

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        self.app.testing = True
        self.ride_data = {
            'ride_id': '1',
            'starting_point': 'kiambu',
            'destination': 'nairobi',
            'date': '02/12/2008',
            'time': '10:00'

        }

        self.empty_ride = {
            'ride_id': '',
            'starting_point': '',
            'destination': '',
            'date': '02/12/2008',
            'time': '10:00'

        }
        

    def test_can_create_a_ride(self):
        '''test api can create a ride (POST request)'''
        result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride_data))
        self.assertEqual(result.status_code, 201)
        self.assertIn('nairobi', str(result.data))

    def test_get_all_rides(self):
        '''test api can get all rides stored (GET request)'''
        result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride_data))
        self.assertEqual(result.status_code, 201)
        result = self.app.get('/api/v1/rides')
        self.assertEqual(result.status_code, 200)
        self.assertIn('nairobi', str(result.data))

    def test_get_ride_by_id(self):
        '''test api can get a single ride by its id (GET request)'''
        post_result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride_data))
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.data.decode())
        result = self.app.get(
            '/api/v1/rides/{}'.format(json_result['ride_id']), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertIn('nairobi', str(result.data))

    def test_edit_non_existing_ride(self):
        '''test api can't edit a non existing ride (PUT request)'''

        self.ride_data['starting_point'] = 'Newest starting_point'
        resp = self.app.put(
            '/api/v1/rides/50000000',
            data=json.dumps(
                self.ride_data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 404)


    def test_edit_a_ride(self):
        '''test api can edit a ride (PUT request)'''
        post_result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride_data))
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.data.decode())
        self.ride_data['starting_point'] = 'Newest starting_point'
        resp = self.app.put(
            '/api/v1/rides/1',
            data=json.dumps(
                self.ride_data),
            content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_delete_a_ride(self):
        '''test api can delete a single ride by id'''
        post_result = self.app.post(
            '/api/v1/rides', data=json.dumps(self.ride_data))
        self.assertEqual(post_result.status_code, 201)
        delete_result = self.app.delete('/api/v1/rides/1')
        self.assertEqual(delete_result.status_code, 200)
        result = self.app.get('/api/v1/rides/1')
        self.assertIn(b'ride Doesnt Exist', result.data)

    def test_rides_cannot_be_blank(self):
        """test api cannot register rides with blank fields"""
        resp = self.app.post('/api/v1/rides',
                                 data=json.dumps(self.empty_ride),
                                 content_type="application/json")

        self.assertIn(b'Please enter correct ride details',resp.data)

    def test_get_non_existent_ride(self):
        '''test api can get a non existing ride by its id (GET request)'''
        post_result = self.app.post(
            '/api/v1/rides',
            data=json.dumps(
                self.ride_data))
        self.assertEqual(post_result.status_code, 201)
        result = self.app.get(
            '/api/v1/rides/500')
        self.assertEqual(result.status_code, 404)

    def test_delete_a_ride(self):
        '''test api can delete a single ride by id'''
        delete_result = self.app.delete('/api/v1/rides/1')
        self.assertEqual(delete_result.status_code, 200)
        result = self.app.get('/api/v1/rides/1')
        self.assertIn(b'ride Doesnt Exist', result.data)


    def tearDown(self):
        self.ride_data.clear()
        print(self.ride_data)


if __name__ == '__main__':
    unittest.main()
