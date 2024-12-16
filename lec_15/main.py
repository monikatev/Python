from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = 'cars.json'

# Utility function to load data from the JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Utility function to save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Route to get all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = load_data()
    return jsonify(cars), 200

# Route to get a car by ID
@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    cars = load_data()
    car = next((car for car in cars if car['id'] == car_id), None)
    if car:
        return jsonify(car), 200
    return jsonify({"error": "Car not found"}), 404

# Route to add a new car
@app.route('/cars', methods=['POST'])
def add_car():
    cars = load_data()
    new_car = request.json
    if not all(key in new_car for key in ('id', 'make', 'model', 'year', 'price')):
        return jsonify({"error": "Invalid car data"}), 400

    if any(car['id'] == new_car['id'] for car in cars):
        return jsonify({"error": "Car with this ID already exists"}), 400

    cars.append(new_car)
    save_data(cars)
    return jsonify(new_car), 201

# Route to update an existing car
@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    cars = load_data()
    updated_car = request.json

    for car in cars:
        if car['id'] == car_id:
            car.update(updated_car)
            save_data(cars)
            return jsonify(car), 200

    return jsonify({"error": "Car not found"}), 404

# Route to delete a car by ID
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    cars = load_data()
    car = next((car for car in cars if car['id'] == car_id), None)

    if car:
        cars.remove(car)
        save_data(cars)
        return jsonify({"message": "Car deleted successfully"}), 200

    return jsonify({"error": "Car not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
