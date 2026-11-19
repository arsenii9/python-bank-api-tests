import pytest
from sqlalchemy.orm import Session
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.db.crud.account_crud import AccountCrudDB as Account


class TestTransfer:
    def test_transfer(self, api_manager, two_accounts, create_user_request, db_session: Session):
        first_account, second_account, second_user = two_accounts

        transfer = TransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=500
        )

        api_manager.user_steps.transfer(user=create_user_request, transfer=transfer)

        first_account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request, account_id=first_account.id
        )
        second_account_state = api_manager.user_steps.get_account_transactions(
            user=second_user, account_id=second_account.id
        )

        assert first_account_state.balance == 2500
        assert second_account_state.balance == 1500

        db_session.expire_all()
        first_account_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_db = Account.get_account_by_id(db_session, second_account.id)

        assert first_account_db is not None, "Счёт отправителя не найден в БД"
        assert second_account_db is not None, "Счёт получателя не найден в БД"
        assert first_account_db.balance == pytest.approx(2500)
        assert second_account_db.balance == pytest.approx(1500)

    def test_transfer_negative(self, api_manager, two_accounts, create_user_request, db_session: Session):
        first_account, second_account, second_user = two_accounts

        transfer = TransferRequest(
            fromAccountId=first_account.id,
            toAccountId=second_account.id,
            amount=499
        )

        api_manager.user_steps.transfer_negative(user=create_user_request, transfer=transfer)

        first_account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request, account_id=first_account.id
        )
        second_account_state = api_manager.user_steps.get_account_transactions(
            user=second_user, account_id=second_account.id
        )

        assert first_account_state.balance == 3000
        assert second_account_state.balance == 1000

        db_session.expire_all()
        first_account_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_db = Account.get_account_by_id(db_session, second_account.id)

        assert first_account_db is not None, "Счёт отправителя не найден в БД"
        assert second_account_db is not None, "Счёт получателя не найден в БД"
        assert first_account_db.balance == pytest.approx(3000)
        assert second_account_db.balance == pytest.approx(1000)
