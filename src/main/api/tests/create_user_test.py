
import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        db_session: Session
    ) -> None:
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username, (
            f"Имя пользователя: ожидалось {create_user_request.username}, получено {response.username}"
        )
        assert create_user_request.role == response.role, (
            f"Роль пользователя: ожидалась {create_user_request.role}, получена {response.role}"
        )

        user_from_db = User.get_user_by_username(
            db_session, create_user_request.username
        )
        assert user_from_db.username == create_user_request.username, (
            f"Имя пользователя в БД: ожидалось {create_user_request.username}, получено {user_from_db.username}"
        )

    @pytest.mark.parametrize(
        "username, password",
        [
            ("a6", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("Maxx1", "Pas!sw0"),
            ("Maxx2", "PAS!SW0RD"),
            ("Maxx3", "PASSSW0RD"),
            ("Maxx4", "PAS!SWRRD"),
            ("", "")
        ]
    )
    def test_create_user_negative(
        self,
        username: str,
        password: str,
        api_manager: ApiManager,
        db_session: Session
    ) -> None:
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
        )

        api_manager.admin_steps.create_user_negative(
            create_user_request=create_user_request
        )

        user_from_db = User.get_user_by_username(
            db_session, create_user_request.username
        )

        assert user_from_db is None, (
            f"Пользователь {username!r} не должен существовать в БД"
        )
