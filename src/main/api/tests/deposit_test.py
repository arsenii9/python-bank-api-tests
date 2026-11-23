
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDB as Account


class TestDeposit:
    def test_deposit(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        create_account: CreateAccountResponse,
        db_session: Session
    ) -> None:
        deposit_request = DepositRequest(
            accountId=create_account.id,
            amount=RandomModelGenerator.generate_amount(1000, 3000)
        )

        response = api_manager.user_steps.deposit_on_account(
            user=create_user_request,
            deposit_request=deposit_request
        )

        account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request,
            account_id=create_account.id
        )

        assert response.balance == deposit_request.amount, (
            f"Баланс после пополнения: {response.balance}, ожидался {deposit_request.amount}"
        )
        assert account_state.balance == deposit_request.amount, (
            f"Баланс счёта: {account_state.balance}, ожидался {deposit_request.amount}"
        )

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, create_account.id)

        assert account_from_db is not None, "Счёт не найден в БД"
        assert account_from_db.balance == pytest.approx(deposit_request.amount), (
            f"Баланс в БД: {account_from_db.balance}, ожидался {deposit_request.amount}"
        )

    def test_deposit_negative(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        create_account: CreateAccountResponse,
        db_session: Session
    ) -> None:
        deposit_request = DepositRequest(
            accountId=create_account.id,
            amount=999
        )

        api_manager.user_steps.deposit_on_account_negative(
            user=create_user_request,
            deposit_request=deposit_request
        )

        account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request,
            account_id=create_account.id
        )

        assert account_state.balance == 0, (
            f"Баланс изменился после отказа API: {account_state.balance}"
        )

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, create_account.id)

        assert account_from_db is not None, "Счёт не найден в БД"
        assert account_from_db.balance == pytest.approx(0), (
            f"Баланс в БД изменился после отказа API: {account_from_db.balance}"
        )
