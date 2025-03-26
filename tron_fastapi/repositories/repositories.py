import time

from requests import HTTPError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron
from tronpy.exceptions import BadAddress
from tronpy.providers import HTTPProvider

from tron_fastapi.config.config import logger, settings
from tron_fastapi.models.tables import AddressRequestORM
from tron_fastapi.schemas.TronSchemas import WalletFromDB


class TronRepo:
    """
    This is class for work with Tron endpoints
    """

    "Create Tronpy client"
    tron_client = Tron(HTTPProvider(api_key=[settings.API_KEY1]))

    @classmethod
    def check_address(cls, address: str) -> bool:
        """
        Checking address for wallet
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
        Get information about wallet
        """
        try:
            account_resource = cls.tron_client.get_account_resource(address)

            # Извлекаем баланс
            balance = round(float(cls.tron_client.get_account_balance(address)), 2)

            # Получаем Bandwidth и Energy

            # Bandwidth
            bandwidth_used = account_resource.get("freeNetLimit", 0)
            total_bandwidth = account_resource.get("NetLimit", 0)
            bandwidth = total_bandwidth - bandwidth_used

            # Energy
            total_energy = account_resource.get("TotalEnergyLimit", 0)
            energy_used = account_resource.get("tronPowerUsed", 0)
            energy = total_energy - energy_used

            # Формируем итоговый словарь
            wallet_info = {"balance": balance, "bandwidth": bandwidth, "energy": energy}

            return wallet_info
        except HTTPError:
            # Данная ошибка связана с бесплатным ключом API. Нужно дождаться доступа
            cls.get_date_by_address(address)


class TronDB:
    """
    This is class for work with database
    """

    @classmethod
    async def get_last_data(
        cls, page: int, page_size: int, session: AsyncSession
    ) -> list:
        """
        Get last data from database with pagination
        """
        query = (
            select(AddressRequestORM)
            .order_by(AddressRequestORM.id.desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        models = await session.execute(query)
        models = models.scalars().all()
        # Convert models to dict
        result = [WalletFromDB.model_validate(model) for model in models]
        return result

    @classmethod
    async def post_new_wallet(
        cls, wallet: AddressRequestORM, session: AsyncSession
    ) -> dict:
        """
        Post new wallet to database
        """
        logger.info(f"Wallet {wallet.address} was created")
        session.add(wallet)
        await session.commit()
