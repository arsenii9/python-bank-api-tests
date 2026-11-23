
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.credit_request_model import CreditRequest


@pytest.fixture
def create_user_request(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_account(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest
) -> CreateAccountResponse:
    response = api_manager.user_steps.create_account(create_user_request)
    return response


@pytest.fixture
def account_with_balance(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest,
    create_account: CreateAccountResponse
) -> CreateAccountResponse:
    deposit_request = DepositRequest(
        accountId=create_account.id,
        amount=RandomModelGenerator.generate_amount(3000, 5000)
    )

    response = api_manager.user_steps.deposit_on_account(
        user=create_user_request,
        deposit_request=deposit_request
    )

    return response


@pytest.fixture
def two_accounts(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest,
    account_with_balance: CreateAccountResponse
) -> tuple[CreateAccountResponse, CreateAccountResponse, CreateUserRequest]:
    second_user = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(second_user)

    second_account = api_manager.user_steps.create_account(second_user)

    deposit_request = DepositRequest(
        accountId=second_account.id,
        amount=RandomModelGenerator.generate_amount(1000, 2000)
    )

    second_account_with_balance = api_manager.user_steps.deposit_on_account(
        user=second_user,
        deposit_request=deposit_request
    )

    return account_with_balance, second_account_with_balance, second_user


@pytest.fixture
def credit_user(api_manager: ApiManager) -> CreateUserRequest:
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    api_manager.admin_steps.create_user(user_request)

    return user_request


@pytest.fixture
def credit_account(
    api_manager: ApiManager,
    credit_user: CreateUserRequest
) -> CreateAccountResponse:
    response = api_manager.user_steps.create_account(credit_user)
    return response


@pytest.fixture
def active_credit(
    api_manager: ApiManager,
    credit_user: CreateUserRequest,
    credit_account: CreateAccountResponse
):
    credit_request = CreditRequest(
        accountId=credit_account.id,
        amount=RandomModelGenerator.generate_amount(5000, 7000),
        termMonths=12
    )

    response = api_manager.user_steps.request_credit(
        user=credit_user,
        credit_request=credit_request
    )

    return response
