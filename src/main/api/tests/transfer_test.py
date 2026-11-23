
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDB as Account


class TestTransfer:
    def test_transfer(
        self,
        api_manager: ApiManager,
        two_accounts: tuple[CreateAccountResponse, CreateAccountResponse, CreateUserRequest],
        create_user_request: CreateUserRequest,
        db_session: Session
    ) -> None:
        first_account, second_account, second_user = two_accounts

        amount = RandomModelGenerator.generate_amount(500, 1000)

        transfer = TransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=amount
        )

        expected_first_balance = first_account.balance - amount
        expected_second_balance = second_account.balance + amount

        api_manager.user_steps.transfer(user=create_user_request, transfer=transfer)

        first_account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request, account_id=first_account.id
        )
        second_account_state = api_manager.user_steps.get_account_transactions(
            user=second_user, account_id=second_account.id
        )

        assert first_account_state.balance == expected_first_balance, (
            f"Баланс отправителя: {first_account_state.balance}, ожидался {expected_first_balance}"
        )
        assert second_account_state.balance == expected_second_balance, (
            f"Баланс получателя: {second_account_state.balance}, ожидался {expected_second_balance}"
        )

        db_session.expire_all()
        first_account_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_db = Account.get_account_by_id(db_session, second_account.id)

        assert first_account_db is not None, "Счёт отправителя не найден в БД"
        assert second_account_db is not None, "Счёт получателя не найден в БД"
        assert first_account_db.balance == pytest.approx(expected_first_balance), (
            f"Баланс отправителя в БД: {first_account_db.balance}, ожидался {expected_first_balance}"
        )
        assert second_account_db.balance == pytest.approx(expected_second_balance), (
            f"Баланс получателя в БД: {second_account_db.balance}, ожидался {expected_second_balance}"
        )

    def test_transfer_negative(
        self,
        api_manager: ApiManager,
        two_accounts: tuple[CreateAccountResponse, CreateAccountResponse, CreateUserRequest],
        create_user_request: CreateUserRequest,
        db_session: Session
    ) -> None:
        first_account, second_account, second_user = two_accounts

        transfer = TransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=499
        )

        expected_first_balance = first_account.balance
        expected_second_balance = second_account.balance

        api_manager.user_steps.transfer_negative(user=create_user_request, transfer=transfer)

        first_account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request, account_id=first_account.id
        )
        second_account_state = api_manager.user_steps.get_account_transactions(
            user=second_user, account_id=second_account.id
        )

        assert first_account_state.balance == expected_first_balance, (
            f"Баланс отправителя: {first_account_state.balance}, ожидался {expected_first_balance}"
        )
        assert second_account_state.balance == expected_second_balance, (
            f"Баланс получателя: {second_account_state.balance}, ожидался {expected_second_balance}"
        )

        db_session.expire_all()
        first_account_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_db = Account.get_account_by_id(db_session, second_account.id)

        assert first_account_db is not None, "Счёт отправителя не найден в БД"
        assert second_account_db is not None, "Счёт получателя не найден в БД"
        assert first_account_db.balance == pytest.approx(expected_first_balance), (
            f"Баланс отправителя в БД: {first_account_db.balance}, ожидался {expected_first_balance}"
        )
        assert second_account_db.balance == pytest.approx(expected_second_balance), (
            f"Баланс получателя в БД: {second_account_db.balance}, ожидался {expected_second_balance}"
        )
