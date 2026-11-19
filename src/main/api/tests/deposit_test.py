import pytest
from sqlalchemy.orm import Session
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDB as Account


class TestDeposit:
    def test_deposit(self, api_manager, create_user_request, create_account, db_session: Session):
        deposit_request = DepositRequest(
            accountId=create_account.id,
            amount=1000
        )

        response = api_manager.user_steps.deposit_on_account(
            user=create_user_request,
            deposit_request=deposit_request
        )

        account_state = api_manager.user_steps.get_account_transactions(
            user=create_user_request,
            account_id=create_account.id
        )

        assert response.balance == 1000
        assert account_state.balance == 1000

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, create_account.id)

        assert account_from_db is not None, "Счёт не найден в БД"
        assert account_from_db.balance == pytest.approx(1000)

    def test_deposit_negative(self, api_manager, create_user_request, create_account, db_session: Session):
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

        assert account_state.balance == 0

        db_session.expire_all()
        account_from_db = Account.get_account_by_id(db_session, create_account.id)

        assert account_from_db is not None, "Счёт не найден в БД"
        assert account_from_db.balance == pytest.approx(0)
