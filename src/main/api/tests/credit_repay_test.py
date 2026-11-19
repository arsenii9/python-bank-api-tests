import pytest
from sqlalchemy.orm import Session
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit
from src.main.api.db.crud.account_crud import AccountCrudDB as Account


class TestRepayCredit:
    def test_repay_credit(self, api_manager, credit_user, credit_account, active_credit, db_session: Session):
        repay_request = RepayCreditRequest(
            creditId=active_credit.creditId,
            accountId=credit_account.id,
            amount=5000
        )

        response = api_manager.user_steps.repay_credit(
            user=credit_user,
            repay_request=repay_request
        )

        credit_stage = api_manager.user_steps.get_credit_history(user=credit_user)

        assert response.creditId == active_credit.creditId
        assert response.amountDeposited == 5000

        credit = credit_stage.credits[0]

        assert credit.creditId == active_credit.creditId
        assert credit.balance == 0

        db_session.expire_all()
        credit_from_db = Credit.get_credit_by_id(db_session, active_credit.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.balance == pytest.approx(0)

    def test_repay_credit_negative(self, api_manager, credit_user, credit_account, active_credit, db_session: Session):
        repay_request = RepayCreditRequest(
            creditId=active_credit.creditId,
            accountId=credit_account.id,
            amount=5000
        )

        api_manager.user_steps.repay_credit(
            user=credit_user,
            repay_request=repay_request
        )

        balance_before = api_manager.user_steps.get_account_transactions(
            user=credit_user,
            account_id=credit_account.id
        )

        db_session.expire_all()
        account_before_db = Account.get_account_by_id(db_session, credit_account.id)
        credit_before_db = Credit.get_credit_by_id(db_session, active_credit.creditId)

        assert account_before_db is not None
        assert credit_before_db is not None

        db_balance_before = account_before_db.balance
        db_credit_balance_before = credit_before_db.balance

        api_manager.user_steps.repay_credit_negative(
            user=credit_user,
            repay_request=repay_request
        )

        balance_after = api_manager.user_steps.get_account_transactions(
            user=credit_user,
            account_id=credit_account.id
        )

        assert balance_after.balance == balance_before.balance

        db_session.expire_all()
        account_after_db = Account.get_account_by_id(db_session, credit_account.id)
        credit_after_db = Credit.get_credit_by_id(db_session, active_credit.creditId)

        assert account_after_db is not None
        assert credit_after_db is not None

        assert account_after_db.balance == pytest.approx(db_balance_before)
        assert credit_after_db.balance == pytest.approx(db_credit_balance_before)
        assert credit_after_db.balance == pytest.approx(0)
