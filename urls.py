import os


BASE_URL = os.getenv('STELLAR_BASE_URL', 'https://qa-stellarburgers.education-services.ru').rstrip('/')
API_URL = f'{BASE_URL}/api'
