import time

from requests import HTTPError
from tronpy import Tron
from tronpy.exceptions import BadAddress


class TronRepo:
    """
    Репозиторий для работы с эндпоинтами TRON
    """

    "Создам клиент Tronpy"
    tron_client = Tron()

    @classmethod
    def check_address(cls, address: str) -> bool:
        """
        Проверка наличия кошелька по адресу
        :param address: адрес кошелька
        :return: True или False
        """

        # Проверяем наличие кошелька по адресу
        try:
            wallet = cls.tron_client.get_account(address)
            if wallet:
                return True
        except BadAddress:
            # Кошелек не найден, возвращаем сообщение
            return False
        except HTTPError:
            # Данная ошибка связана с бесплатным ключом API. Нужно дождаться доступа
            time.sleep(1)
            return cls.check_address(address)

    @classmethod
    def get_date_by_address(cls, address: str) -> dict:
        """
        Получение информации о кошельке по адресу
        :param address: адрес кошелька
        :return: словарь с информацией о кошельке
        """
        try:
            balance = cls.tron_client.get_account_balance(address)
            bandwidth = cls.tron_client.get_bandwidth(address)
            energy = cls.tron_client.get_account_resource(address)['TotalEnergyLimit']
            result = {"balance": balance, "bandwidth": bandwidth, "energy": energy}
            return result
        except HTTPError:
            # Данная ошибка связана с бесплатным ключом API. Нужно дождаться доступа
            cls.get_date_by_address(address)
