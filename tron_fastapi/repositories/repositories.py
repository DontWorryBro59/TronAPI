import time

from requests import HTTPError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy import Tron
from tronpy.exceptions import BadAddress
from tronpy.providers import HTTPProvider

from tron_fastapi.config.config import logger, settings
from tron_fastapi.models.tables import AddressRequestORM


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
            balance = round(float(cls.tron_client.get_account_balance(address)), 2)
            bandwidth = cls.tron_client.get_bandwidth(address)
            energy = cls.tron_client.get_account_resource(address)["TotalEnergyLimit"]
            result = {"balance": balance, "bandwidth": bandwidth, "energy": energy}
            return result
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
        result = await session.execute(query)
        result = result.scalars().all()
        print(result)

        logger.info(f"Get {page_size} wallets from database")
        logger.info(f"Wallets: {result}")

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
