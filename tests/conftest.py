import pytest

@pytest.fixture
def test_app():
    from app.main import app
    return app