
from collections.abc import Callable
from requests import Response
from http import HTTPStatus


class ResponseSpecs:

    @staticmethod
    def request_ok() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.OK, (
                f"Ожидался статус 200, получен {response.status_code}"
            )
        return confirm

    @staticmethod
    def request_created() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.CREATED, (
                f"Ожидался статус 201, получен {response.status_code}"
            )
        return confirm

    @staticmethod
    def request_bad() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.BAD_REQUEST, (
                f"Ожидался статус 400, получен {response.status_code}"
            )
        return confirm

    @staticmethod
    def request_forbidden() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.FORBIDDEN, (
                f"Ожидался статус 403, получен {response.status_code}"
            )
        return confirm

    @staticmethod
    def request_unprocessable_entity() -> Callable[[Response], None]:
        def confirm(response: Response) -> None:
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
                f"Ожидался статус 422, получен {response.status_code}"
            )
        return confirm
