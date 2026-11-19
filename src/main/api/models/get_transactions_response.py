from src.main.api.models.base_model import BaseModel

class Transaction(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: int | None
    toAccountId: int | None
    createdAt: str

class GetTransactionResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transaction]