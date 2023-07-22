import os

from flask import Flask, request

from init_logger import create_logger
from my_bitrix.bitrix_client import bitrix_client

application = Flask(__name__)

logger = create_logger()


@application.route('/sale-capital/webhook', methods=['POST'])
def webhook():
    data = request.form.to_dict()
    bitrix_client.get_crm_deal(data)
    return 'Webhook received successfully'


@application.route('/sale-capital/wolya', methods=['POST'])
def wolya_response():
    """
    Recieve data from wolya instance
    :return:
    """
    try:
        data = request.get_json()
        bitrix_client.create_crm_deal_after_wolya(data)
    except Exception as e:
        logger.error(
            "An error occurred in %s: %s",
            os.path.abspath(__file__),
            str(e),
        )


if __name__ == '__main__':
    application.run(port=5001, host='0.0.0.0')
