from flask import Flask, request, jsonify
from car import APICarManager

app = Flask(__name__)
car_manager = APICarManager()

@app.route('/audi_models', methods=['GET'])
def hyundai_models():
    cars, code = car_manager.audi_ten_yo_cars()
    return jsonify(cars), code

@app.route('/get_brands', methods=['GET'])
def get_brands():
    cars, code = car_manager.get_brands()
    return jsonify(cars), code

@app.route('/get_brand_id', methods=['POST'])
def get_brand_id():

    data = request.get_json()
    brand_name = data.get('brand')
    if not brand_name:
        return jsonify({"error": "brand name is required"}), 400

    brands, code = car_manager.find_brand_id_by_name(brand_name)
    return jsonify(brands), code

@app.route('/get_cars_model', methods=['POST'])
def get_cars_model():
    """POST endpoint to filter cars by brand and model"""
    data = request.get_json()

    brand = data.get('brand')
    model = data.get('model', None)

    if not brand:
        return jsonify({"error": "brand is required"}), 400
    
    cars, code = car_manager.get_car_models(brand, filter_model_id=model)

    return jsonify(cars), code

@app.route('/filter_car_model_year', methods=['POST'])
def filter_cars():
    """POST endpoint to filter cars by brand, model, and year."""
    data = request.get_json()

    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year', None)

    if not all([brand, model]):
        return jsonify({"error": "brand and model are required"}), 400

    filtered_cars, code = car_manager.get_car_model_years(brand, model, filter_years=year)

    return jsonify(filtered_cars), code

if __name__ == '__main__':
    app.run(debug=True)


