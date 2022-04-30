import pytest

proxy = {"http://": "localhost:8080"}


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru/",
        help="This is request url"
    )

    parser.addoption(
        "--status_code",
        type=int,
        default=200,
        choices=[200, 300, 400, 404, 500, 502],
        help="status codes"
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")
