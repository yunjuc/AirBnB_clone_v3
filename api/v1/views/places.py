#!/usr/bin/python3
'''Places API view'''
import json
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.city import City
import sys


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    '''Get places'''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    j_list = []
    for k, v in storage.all('Place').items():
        if v.city_id == city.id:
            j_list.append(v.to_dict())   
    return jsonify(j_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    '''Get place by id'''
    try:
        place = storage.get('Place', place_id)
        return jsonify(place.to_dict())
    except Exception:
        return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place_id(place_id):
    '''Delete place by id'''
    if 'Place.' + place_id in storage.all('Place'):
        place = storage.get('Place', place_id)
        storage.delete(place)
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def post_place():
    '''Create a place'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    elif 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    elif 'name' not in request.get_json():
        abort(400, 'Missing name')
    else:
        place = request.get_json()
        new = Place(**place)
        storage.new(new)
        storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update a place'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if 'Place.' + place_id in storage.all('Place'):
        place = storage.get('Place', place_id)
        data = request.get_json()
        for k, v in data.items():
            if k is not 'id' or\
               k is not 'created_at' or\
               k is not 'updated_at' or\
               k is not 'user_id' or\
               k is not 'city_id':
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
    else:
        return abort(404)
