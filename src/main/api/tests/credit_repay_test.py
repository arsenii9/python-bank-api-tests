
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDB as Credit
from src.main.api.db.crud.account_crud import AccountCrudDB as Account


class TestRepayCredit:
    def test_repay_credit(
        self,
        api_manager: ApiManager,
        credit_user: CreateUserRequest,
        credit_account: CreateAccountResponse,
        active_credit: CreditResponse,
        db_session: Session
    ) -> None:
        repay_request = RepayCreditRequest(
            creditId=active_credit.creditId,
            accountId=credit_account.id,
            amount=active_credit.balance
        )

        response = api_manager.user_steps.repay_credit(
            user=credit_user,
            repay_request=repay_request
        )

        credit_stage = api_manager.user_steps.get_credit_history(user=credit_user)

        assert response.creditId == active_credit.creditId, (
            "ID погашенного кредита не совпадает"
        )
        assert response.amountDeposited == repay_request.amount, (
            f"Сумма погашения: {response.amountDeposited}, ожидалось {repay_request.amount}"
        )

        credit = credit_stage.credits[0]

        assert credit.creditId == active_credit.creditId, (
            "ID кредита в истории не совпадает"
        )
        assert credit.balance == 0, (
            f"Остаток кредита: {credit.balance}, ожидался 0"
        )

        db_session.expire_all()
        credit_from_db = Credit.get_credit_by_id(db_session, active_credit.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.balance == pytest.approx(0), (
            f"Остаток кредита в БД: {credit_from_db.balance}, ожидался 0"
        )

    def test_repay_credit_negative(
        self,
        api_manager: ApiManager,
        credit_user: CreateUserRequest,
        credit_account: CreateAccountResponse,
        active_credit: CreditResponse,
        db_session: Session
    ) -> None:
        repay_request = RepayCreditRequest(
            creditId=active_credit.creditId,
            accountId=credit_account.id,
            amount=active_credit.balance
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

        assert account_before_db is not None, "Счёт не найден в БД"
        assert credit_before_db is not None, "Кредит не найден в БД"

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

        assert balance_after.balance == balance_before.balance, (
            f"Баланс счёта изменился: {balance_before.balance} → {balance_after.balance}"
        )

        db_session.expire_all()
        account_after_db = Account.get_account_by_id(db_session, credit_account.id)
        credit_after_db = Credit.get_credit_by_id(db_session, active_credit.creditId)

        assert account_after_db is not None, "Счёт не найден в БД после погашения"
        assert credit_after_db is not None, "Кредит не найден в БД после погашения"

        assert account_after_db.balance == pytest.approx(db_balance_before), (
            f"Баланс счёта в БД изменился: {db_balance_before} → {account_after_db.balance}"
        )
        assert credit_after_db.balance == pytest.approx(db_credit_balance_before), (
            f"Баланс кредита в БД изменился: {db_credit_balance_before} → {credit_after_db.balance}"
        )
        assert credit_after_db.balance == pytest.approx(0), (
            f"Кредит в БД не погашен: остаток {credit_after_db.balance}"
        )
