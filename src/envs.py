from enum import Enum

import dotenv

envs = dotenv.dotenv_values()


class Envs(Enum):
    WOLYA_URL: str = envs.get("WOLYA_URL")

    EMAIL_ACCOUNT: str = envs.get('EMAIL_ACCOUNT')
    EMAIL_PASSWORD: str = envs.get('EMAIL_PASSWORD')

    BITRIX_WEBHOOK: str = envs.get('BITRIX_WEBHOOK')

    BITRIX_DOMAIN: str = envs.get('BITRIX_DOMAIN')
    BITRIX_CLIENT_SECRET: str = envs.get('BITRIX_CLIENT_SECRET')
    BITRIX_CLIENT_ID: str = envs.get('BITRIX_CLIENT_ID')

    BITRIX_ALIBABA_PRODUCTS: str = envs.get('BITRIX_ALIBABA_PRODUCTS')
    API_KEY: str = envs.get('API_KEY')
