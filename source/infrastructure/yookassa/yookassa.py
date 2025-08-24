import httpx
import logging
import uuid

logger = logging.getLogger(__name__)



class YooKassaClient:

    BASE_URL="https://api.yookassa.ru/v3/payments"

    def __init__(self, store_id, store_token):
        self.store_id = str(store_id)
        self.store_token = str(store_token)

    async def create_payment(self, amount: str, description: str, customer_contact: dict):

        idempotence_key = str(uuid.uuid4())


        """Create payment in yookassa service
            Args:

            amount: str

            description: str
        """

        headers = {
            'Idempotence-Key': idempotence_key,
            'Content-Type': 'application/json',
        }

        json_data = {
            'amount': {
                'value': amount,
                'currency': 'RUB',
            },
            'payment_method_data': {
                'type': 'bank_card',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://t.me/trauma_aibot',
            },
            'description': description,
            'capture': True,
            'receipt': {
                'customer': customer_contact,
                'items': [
                    {
                        'description': description, 
                        'quantity': '1.000',
                        'amount': {
                            'value': amount,
                            'currency': 'RUB',
                        },
                        'vat_code': 1,  # 1 - без НДС; измените на подходящий (2 - 0%, 3 - 10%, 4 - 20%, etc.)
                        'payment_subject': 'service',  # Для услуг/подписок
                        'payment_mode': 'full_payment',  # Полная оплата
                    }
                ],
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.BASE_URL,
                                            headers=headers,
                                            json=json_data,
                                            auth=(self.store_id, self.store_token))
                response.raise_for_status()
                response_data = response.json()
                return (response_data.get("confirmation", {}).get("confirmation_url"), response_data.get("id", ""))
            except:
                logger.error(f'Error when create payment {amount} {description} {response.text}')
                raise
