from flask import Flask, request, jsonify
from car import APICarManager

app = Flask(__name__)
car_manager = APICarManager()

@app.route('/hyundai_models', methods=['GET'])
def hyundai_models():
    cars, code = car_manager.hyundai_ten_yo_cars()
    return jsonify(cars), code

@app.route('/get_cars_model', methods=['POST'])
def get_cars_model():
    """POST endpoint to filter cars by brand, model, and year."""
    data = request.get_json()

    brand = data.get('brand')
    model = data.get('model')

    if not all([brand, model]):
        return jsonify({"error": "brand, model, and year are required"}), 400

    cars, code = car_manager.get_car_model(brand, model)
    if code != 200:
        return jsonify({"error": cars}), code

    return jsonify(cars), code

@app.route('/filter_cars_year', methods=['POST'])
def filter_cars():
    """POST endpoint to filter cars by brand, model, and year."""
    data = request.get_json()

    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')

    if not all([brand, model, year]):
        return jsonify({"error": "brand, model, and year are required"}), 400

    cars, code = car_manager.get_car_model(brand, model)
    if code != 200:
        return jsonify({"error": cars}), code

    filtered_cars, code = car_manager.filter_car_model_years(cars, year)
    return jsonify(filtered_cars), code

if __name__ == '__main__':
    app.run(debug=True)


