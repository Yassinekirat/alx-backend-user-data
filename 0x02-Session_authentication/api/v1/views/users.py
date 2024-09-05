#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views

@app_views.route('/api/v1/users', methods=['GET'])
def get_users():
    """Retrieve all users"""
    users = User().all()
    return jsonify([user.to_json() for user in users]), 200

@app_views.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by user_id"""
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json()), 200
    
    user = User().find(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json()), 200

@app_views.route('/api/v1/users', methods=['POST'])
def create_user():
    """Create a new user"""
    # Add code to handle user creation
    pass

@app_views.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user by user_id"""
    # Add code to handle user update
    pass

@app_views.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by user_id"""
    # Add code to handle user deletion
    pass
