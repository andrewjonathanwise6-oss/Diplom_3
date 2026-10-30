from dataclasses import dataclass, field
from uuid import uuid4

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from urls import API_URL


@dataclass
class TestUser:
    email: str
    name: str
    password: str = field(repr=False)
    access_token: str = field(default='', repr=False)

    @classmethod
    def unique(cls):
        return cls(email=f'diplom3_{uuid4().hex}@example.com', name='Diplom UI', password=uuid4().hex)


class ApiClient:
    """API только для подготовки/удаления данных; заказы оформляются через UI."""

    def __init__(self):
        self.session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.5, status_forcelist=(502, 503, 504), allowed_methods=('GET', 'DELETE'))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def request(self, method, path, **kwargs):
        response = self.session.request(method, API_URL + path, timeout=(10, 30), **kwargs)
        response.raise_for_status()
        data = response.json()
        if data.get('success') is not True:
            raise RuntimeError(f'{method} {path}: {data.get("message", "success != true")}')
        return response.status_code, data

    def register(self, user):
        _, data = self.request(
            'POST', '/auth/register',
            json={'email': user.email, 'password': user.password, 'name': user.name},
        )
        user.access_token = data['accessToken']

    def delete_user(self, user):
        # При неоднозначном ответе регистрации ищем созданный аккаунт по его данным.
        if not user.access_token:
            response = self.session.post(
                API_URL + '/auth/login',
                json={'email': user.email, 'password': user.password}, timeout=(10, 30),
            )
            if response.status_code == 401:
                return 'Аккаунт не был создан'
            response.raise_for_status()
            user.access_token = response.json()['accessToken']
        status, data = self.request('DELETE', '/auth/user', headers={'Authorization': user.access_token})
        return f'{status}: {data.get("message", "removed")}'

    def close(self):
        self.session.close()
