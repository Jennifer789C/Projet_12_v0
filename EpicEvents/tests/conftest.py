from django.contrib.auth import get_user_model
import pytest


@pytest.fixture()
def Personnel():
    Personnel = get_user_model()
    return Personnel
