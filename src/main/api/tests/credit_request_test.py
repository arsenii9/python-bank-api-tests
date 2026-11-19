import pytest
from sqlalchemy.orm import Session
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit


class TestCreditRequest:
    def test_credit_request(self, api_manager, credit_user, credit_account, db_session: Session):
        credit_request = CreditRequest(
            accountId=credit_account.id,
            amount=5000,
            termMonths=3
        )

        response = api_manager.user_steps.request_credit(
            user=credit_user,
            credit_request=credit_request
        )

        credit_history = api_manager.user_steps.get_credit_history(user=credit_user)
        credit = credit_history.credits[0]

        assert credit.creditId == response.creditId
        assert credit.accountId == credit_account.id
        assert credit.amount == 5000

        db_session.expire_all()
        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.account_id == credit_account.id
        assert credit_from_db.amount == pytest.approx(5000)
        assert credit_from_db.term_months == 3

    def test_credit_request_negative(self, api_manager, create_user_request, create_account, db_session: Session):
        credit_request = CreditRequest(
            accountId=create_account.id,
            amount=5000,
            termMonths=3
        )

        api_manager.user_steps.request_credit_negative(
            user=create_user_request,
            credit_request=credit_request
        )

        db_session.expire_all()
        credits_from_db = Credit.get_credits_by_account_id(
            db_session, create_account.id
        )

        assert len(credits_from_db) == 0, "Кредит был создан несмотря на отказ API"
