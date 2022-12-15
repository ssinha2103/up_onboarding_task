# import pytest
# from rest_framework.test import APIClient
# from django.contrib.auth import get_user_model
#
# client = APIClient()
# User = get_user_model()
#
# @pytest.fixture()
# def merchant():
#     return User.objects.create_user(name = "S", username = "ss", password = "password")
#
# def test(merchant):
#     response = client.post('/register/', dict(name = "S", username = 'ss', password = "password"))
#     assert response.status_code == 201
