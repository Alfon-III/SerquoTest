
import requests
import logging

class APICarManager():

    def __init__(self):
        # Docummentaciion API: https://deividfortuna.github.io/fipe/v2/#tag/Fipe
        self.base_url = 'https://parallelum.com.br/fipe/api/v1/'
        self.fipe_url  =  'https://fipe.parallelum.com.br/api/v2/'

    def audi_ten_yo_cars(self):
        """Hardcoded functionn to get hyundai model cars prior to 2015"""
        brand_name = 'Audi'
        model_name = 'A1'
        
        # 1. Get the brand id for "Audi" 
        brand_id, code = self.find_brand_id_by_name(brand_name)
        if not brand_id:
            logging.error(f"Could not find brand '{brand_name}' id inn  API")
            return f"Could not find brand '{brand_name}' id inn  API", code
        
        # 2. Find all models for Audi,  also filter by the knnown model name "A1"
        car_models, code = self.get_car_models(brand_id, filter_model_name=model_name)
        if code != 200:
            return car_models, code
        
        # 3. As there can be multiple models for A1, get the first one
        car_model = car_models[0]
        car_model_year, code = self.get_car_model_years(brand_id, car_model['code'], filter_years=2010)
        return car_model_year, code

    def get_brands(self):

        url = f'{self.fipe_url}cars/brands/'
        respose = requests.get(url)

        if respose.status_code != 200:
            print('Error at getting car brands list')
            return respose.text, respose.status_code
        
        return respose.json(), respose.status_code
    
    def find_brand_id_by_name(self, brand_name):
        brands, code = self.get_brands()

        if code == 200:    
            for brand in brands:
                if brand_name in brand['name']:
                    return brand['code'], 200
                
        return f"Could not find brand:  '{brand_name}'", 400

    def get_car_models(self, brand: int, filter_model_id: int = None, filter_model_name:str = ''):
        

        url = f'{self.fipe_url}cars/brands/{brand}/models'
        print(url)
        respose = requests.get(url)

        if respose.status_code != 200:
            print('Error at getting car model list')
            return respose.text, respose.status_code
        
        models_car = respose.json()

        if filter_model_name:
            filtered_models = []
            for car in models_car:
                if filter_model_name in car['name']:
                    filtered_models.append(car)
            return filtered_models, respose.status_code 

        if filter_model_id:
            for car in models_car:
                if car['code'] == str(filter_model_id):
                    return car, respose.status_code
        
        return models_car, respose.status_code

    def get_car_model_years(self, brand: int, model: int, filter_years: int = None):
        """Get models from a car brand filtered by year

        Args:
            brand (int): id number of the car brand
            model (int): id of the model of the brand
        Returns:
            _type_: _description_
        """

        url = f'{self.base_url}carros/marcas/{brand}/modelos/{model}/anos'

        respose = requests.get(url)
        
        if respose.status_code != 200:
            print('Error at getting car list')
            return respose.text, respose.status_code
        
        models_year = respose.json()

        if filter_years:
            try: 
                filtered_model_year = []

                for model_year in models_year:
                    if int(model_year['codigo'].split('-')[0]) >= filter_years:
                        filtered_model_year.append(model_year)

            except KeyError as e:
                logging.error(f'Missing key "codigo" in data: {e}')
                return str(e), 400
            except (TypeError, ValueError) as e:
                logging.error(f"Data type issue: {e}")
                return str(e), 400
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                return str(e), 500

            return filtered_model_year, 200
        
        return respose.json(), respose.status_code

# car = APICarManager()
# print(car.audi_ten_yo_cars())
