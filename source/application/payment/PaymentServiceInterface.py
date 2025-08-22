from abc import ABC, abstractmethod



class PaymentServiceInterface(ABC):

    @abstractmethod
    async def create_payment(self, amount: int, description: str):
        ...