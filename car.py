
import requests
import logging

class APICarManager():

    def __init__(self):
        # Docummentaciion API: https://deividfortuna.github.io/fipe/v2/#tag/Fipe
        self.base_url = 'https://parallelum.com.br/fipe/api/v1/'

    def hyundai_ten_yo_cars(self):
        """Hardcoded functionn to get hyundai model cars prior to 2015"""

        hyundai_cars, code = self.get_car_model(59, 5940)
        if code != 200:
            return hyundai_cars, code    
            
        return self.filter_car_model_years(hyundai_cars, 2015)

                
    def get_car_model(self, brand: int, model: int):
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
        
        return respose.json(), respose.status_code

    def filter_car_model_years(self, models_year: list, year: int):
        """Filter the models by year greater or equal than the year provided

        Args:
            models_year (list): 
            year (int): years gte to filter

        Returns:
            _type_: filtered list
        """
        filtered_cars = []

        if not models_year:
            return filtered_cars

        try: 
            for car in models_year:
                if int(car['codigo'].split('-')[0]) >= year:
                    filtered_cars.append(car)

        except KeyError as e:
            logging.error(f'Missing key "codigo" in data: {e}')
            return str(e), 400
        except (TypeError, ValueError) as e:
            logging.error(f"Data type issue: {e}")
            return str(e), 400
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return str(e), 500

        return filtered_cars, 200

