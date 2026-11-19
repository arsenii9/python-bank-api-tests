
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.get_transactions_response import GetTransactionResponse
from src.main.api.models.transfer_request_model import TransferRequest
from src.main.api.models.credit_request_model import CreditRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest

from src.main.api.specs.base_steps import BaseSteps
from src.main.api.specs.requests_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs



class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post(create_user_request)
        return response

    def deposit_on_account(self, user: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.DEPOSIT_ON_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def deposit_on_account_negative(self, user: CreateUserRequest, deposit_request: DepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.DEPOSIT_ON_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response

    def get_account_transactions(self, user: CreateUserRequest, account_id: int):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.GET_ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_ok()
        ).get(account_id)
        return response


    def transfer(self, user: CreateUserRequest, transfer: TransferRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer)
        return response

    def transfer_negative(self, user: CreateUserRequest, transfer: TransferRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_bad()
        ).post(transfer)
        return response

    def request_credit(self, user: CreateUserRequest, credit_request: CreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response


    def request_credit_negative(self, user: CreateUserRequest, credit_request: CreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.request_forbidden()
        ).post(credit_request)
        return response

    def repay_credit(self, user: CreateUserRequest, repay_request: RepayCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(repay_request)
        return response

    def repay_credit_negative(self, user: CreateUserRequest, repay_request: RepayCreditRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable_entity()
        ).post(repay_request)
        return response


    def get_credit_history(self, user: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user.username, password=user.password),
            Endpoint.CREDIT_HISTORY,
            ResponseSpecs.request_ok()
        ).get()
        return response
