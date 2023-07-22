import os

import requests
from bitrix24 import *

from init_logger import create_logger
from src.dtos.wolya_dto import WolyaDTO
from src.enums.bitrix_enum import BitrixEnum
from envs import Envs
from src.smtp.mailing import mailing

event_counter = 0
logger = create_logger()


class BitrixClient:
    deal_key = 'data[FIELDS][ID]'

    def __init__(self):
        self.__wolya_url = Envs.WOLYA_URL.value
        self.__bitrix_client = Bitrix24(Envs.BITRIX_WEBHOOK.value)

    def get_crm_deal(self, crm_deal):
        global event_counter
        event_counter += 1
        try:
            if event_counter <= 1:
                deals = self.__bitrix_client.callMethod('crm.deal.list',
                                                        order={'STAGE_ID': 'ASC'})
                current_deal = None
                for deal in deals:
                    if deal['ID'] == crm_deal[self.deal_key] and BitrixEnum.from_form.value in deal['TITLE']:
                        current_deal = deal
                        break
                return current_deal
        except Exception as e:
            logger.error(
                "An error occurred in webhook %s: %s",
                os.path.abspath(__file__),
                str(e),
            )

    def _send_mail_and_request(self, current_deal):
        try:
            if current_deal:
                mailing.send_email()
                amazon_urls = current_deal.get('COMMENTS', None)
                deal_id = current_deal.get('ID')
                if amazon_urls:
                    for url in amazon_urls:
                        self.__send_request_to_wolya_instance_after_event(params={"amazon": url, "deal_id": deal_id})
        except Exception as e:
            logger.error(
                "An error occurred in sending request to wolya %s: %s",
                os.path.abspath(__file__),
                str(e),
            )

    def __send_request_to_wolya_instance_after_event(self, params):
        requests.get(url=self.__wolya_url,
                     params=WolyaDTO(amazonUrl=params.get('amazon'), dealId=params.get('deal_id')).dict(by_alias=True),
                     timeout=1)

    def create_crm_deal_after_wolya(self, data):
        # Update the deal by its ID
        if data:
            updated_fields = {
                Envs.BITRIX_ALIBABA_PRODUCTS.value: "\n".join(str(item) for item in data)
            }

            self.__bitrix_client.callMethod("crm.deal.update", id=data[0].get('dealId'), fields=updated_fields)


bitrix_client = BitrixClient()
