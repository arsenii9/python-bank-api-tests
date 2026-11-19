from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from typing import Type, Optional
from dataclasses import dataclass
from enum import Enum

from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.get_transactions_response import GetTransactionResponse
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.models.transfer_response_model import TransferResponse
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.models.credit_history_response import CreditHistoryResponse

@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    DEPOSIT_ON_ACCOUNT = EndpointConfiguration(
        request_model=DepositRequest,
        url="/account/deposit",
        response_model=DepositResponse
    )

    GET_ACCOUNT_TRANSACTIONS = EndpointConfiguration(
        request_model= None,
        url="/account/transactions/",
        response_model=GetTransactionResponse

    )

    TRANSFER = EndpointConfiguration(
        request_model=TransferRequest,
        url="/account/transfer",
        response_model=TransferResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        request_model=CreditRequest,
        url="/credit/request",
        response_model=CreditResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model=RepayCreditRequest,
        url="/credit/repay",
        response_model=RepayCreditResponse
    )

    CREDIT_HISTORY = EndpointConfiguration(
        request_model=None,
        url="/credit/history",
        response_model=CreditHistoryResponse
    )