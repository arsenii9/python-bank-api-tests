from src.main.api.models.base_model import BaseModel


class CreditResponse(BaseModel):
    # В Swagger указано accountId, но фактически API возвращает id.
    # Возможно это баг, мне придется использовать фактическое поведение чтобы не получать ошибки валидации.
    id: int
    amount: float
    termMonths: int
    balance: float
    creditId: int