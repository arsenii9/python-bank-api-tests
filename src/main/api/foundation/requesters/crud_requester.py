from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from typing import Optional
from requests import Response
import requests
import allure
from src.main.api.configs.config import Config

class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response:
        body = model.model_dump() if model is not None else ""
        with allure.step(f"POST {self.endpoint.value.url}"):
            response = requests.post(
                url=f"{Config.fetch('backend_url')}{self.endpoint.value.url}",
                headers=self.request_spec,
                json=body
            )
            self.response_spec(response)
        return response

    def delete(self, user_id: int) -> BaseModel | Response:
        with allure.step(f"DELETE {self.endpoint.value.url}/{user_id}"):
            response = requests.delete(
                url=f"{Config.fetch('backend_url')}{self.endpoint.value.url}/{user_id}",
                headers=self.request_spec
            )
            self.response_spec(response)
        return response

    def get(self, account_id: int | None = None) -> BaseModel | Response:
        suffix = str(account_id) if account_id is not None else ""
        with allure.step(f"GET {self.endpoint.value.url}{suffix}"):
            response = requests.get(
                url=f"{Config.fetch('backend_url')}{self.endpoint.value.url}{suffix}",
                headers=self.request_spec
            )
            self.response_spec(response)
        return response
