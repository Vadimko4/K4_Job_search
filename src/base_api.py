from abc import ABC, abstractmethod


class BaseApi(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def api_connections(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass
