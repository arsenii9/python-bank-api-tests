
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit


class TestCreditRequest:
    def test_credit_request(
        self,
        api_manager: ApiManager,
        credit_user: CreateUserRequest,
        credit_account: CreateAccountResponse,
        db_session: Session
    ) -> None:
        credit_request = CreditRequest(
            accountId=credit_account.id,
            amount=RandomModelGenerator.generate_amount(5000, 7000),
            termMonths=3
        )

        response = api_manager.user_steps.request_credit(
            user=credit_user,
            credit_request=credit_request
        )

        credit_history = api_manager.user_steps.get_credit_history(user=credit_user)
        credit = credit_history.credits[0]

        assert credit.creditId == response.creditId, (
            "ID кредита в истории не совпадает с ответом API"
        )
        assert credit.accountId == credit_account.id, (
            "Кредит привязан к неверному счёту"
        )
        assert credit.amount == credit_request.amount, (
            f"Сумма кредита: {credit.amount}, ожидалось {credit_request.amount}"
        )

        db_session.expire_all()
        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.account_id == credit_account.id, (
            "ID счёта кредита в БД не совпадает"
        )
        assert credit_from_db.amount == pytest.approx(credit_request.amount), (
            f"Сумма кредита в БД: {credit_from_db.amount}, ожидалось {credit_request.amount}"
        )
        assert credit_from_db.term_months == credit_request.termMonths, (
            f"Срок кредита в БД: {credit_from_db.term_months}, ожидалось {credit_request.termMonths}"
        )

    def test_credit_request_negative(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        create_account: CreateAccountResponse,
        db_session: Session
    ) -> None:
        credit_request = CreditRequest(
            accountId=create_account.id,
            amount=RandomModelGenerator.generate_amount(5000, 7000),
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

        assert len(credits_from_db) == 0, (
            f"Кредит создан несмотря на отказ API: найдено {len(credits_from_db)}"
        )
