
import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.credit_request_model import CreditRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_account(api_manager, create_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    return response


@pytest.fixture
def account_with_balance(api_manager, create_user_request, create_account):
    deposit_request = DepositRequest(
        accountId=create_account.id,
        amount=3000
    )

    response = api_manager.user_steps.deposit_on_account(
        user=create_user_request,
        deposit_request=deposit_request
    )

    return response


@pytest.fixture
def two_accounts(api_manager, create_user_request, account_with_balance):
    second_user = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(second_user)

    second_account = api_manager.user_steps.create_account(second_user)

    deposit_request = DepositRequest(
        accountId=second_account.id,
        amount=1000
    )

    second_account_with_balance = api_manager.user_steps.deposit_on_account(
        user=second_user,
        deposit_request=deposit_request
    )

    return account_with_balance, second_account_with_balance, second_user


@pytest.fixture
def credit_user(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"

    api_manager.admin_steps.create_user(user_request)

    return user_request


@pytest.fixture
def credit_account(api_manager, credit_user):
    response = api_manager.user_steps.create_account(credit_user)
    return response


@pytest.fixture
def active_credit(api_manager, credit_user, credit_account):
    credit_request = CreditRequest(
        accountId=credit_account.id,
        amount=5000,
        termMonths=12
    )

    response = api_manager.user_steps.request_credit(
        user=credit_user,
        credit_request=credit_request
    )

    return response
