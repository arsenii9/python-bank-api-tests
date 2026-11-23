
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestLogin:
    def test_login_admin(self, api_manager: ApiManager) -> None:
        login_test_user = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_test_user)

        assert login_test_user.username == response.user.username, (
            f"Имя администратора: ожидалось {login_test_user.username}, получено {response.user.username}"
        )
        assert response.user.role == "ROLE_ADMIN", (
            f"Роль администратора: ожидалась ROLE_ADMIN, получена {response.user.role}"
        )

    def test_login_user(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest
    ) -> None:
        response = api_manager.admin_steps.login_user(create_user_request)

        assert response.user.username == create_user_request.username, (
            f"Имя пользователя: ожидалось {create_user_request.username}, получено {response.user.username}"
        )
        assert response.user.role == "ROLE_USER", (
            f"Роль пользователя: ожидалась ROLE_USER, получена {response.user.role}"
        )
