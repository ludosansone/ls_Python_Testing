import pytest
from flask import request
from tests.fixtures import client
from server import loadClubs, loadCompetitions


@pytest.mark.usefixtures("client")
class TestData:
    @pytest.mark.parametrize("function", [
        (loadClubs),
        (loadCompetitions)
    ])
    def test_should_return_not_none(self, function):
        """
            Test si les fonctions chargeant les données ne retournent pas None
        """

        response = function()
        assert response is not None

    @pytest.mark.parametrize("places, status_code", [
        (50, 302),
        (13, 302),
        (12, 200)
    ])
    def test_should_match_with_status_code(self, client, places, status_code):
        data = {
            'club': 'Simply Lift',
            'competition': 'Fall Classic',
            'places': places
        }

        response = client.post('/purchasePlaces', data=data)

        assert response.status_code == status_code
