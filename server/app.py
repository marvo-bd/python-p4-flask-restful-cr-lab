#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        '''Returns a list of all plants as JSON.'''
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        '''Creates a new plant and returns it as JSON.'''
        data = request.get_json()
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
        )
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201

class PlantByID(Resource):
    def get(self, id):
        '''Returns a plant by ID as JSON.'''
        plant = Plant.query.get_or_404(id)
        return plant.to_dict(), 200

    def delete(self, id):
        '''Deletes a plant by ID.'''
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return '', 204

# Add resources to API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
