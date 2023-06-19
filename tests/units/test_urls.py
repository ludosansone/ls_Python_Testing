import pytest
from tests.fixtures import client


@pytest.mark.usefixtures("client")
class TestURLs:
    @pytest.mark.parametrize("url", [
        ('/'),
        ('/board'),
    ])
    def test_should_return_200(self, client, url):
        """
            Test que le code retourné est bien 200,
            nous vérifions ainsi que l'url indiquée existe bien, et qu'elle répond normalement.
        """

        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.parametrize("url", [
        ('/showSummary'),
        ('/purchasePlaces')
    ])
    def test_should_return_405(self, client, url):
        """
            Test que le code retourné est bien 405,
            nous vérifions ainsi que la méthode get est bien rejeté à l'url indiquée.
        """

        response = client.get(url)
        assert response.status_code == 405

    @pytest.mark.parametrize("url, data, status_code", [
        ('/showSummary', {'email': 'john@simplylift.co'}, 200),
        ('/showSummary', {'email': ''}, 302),
        ('/showSummary', {'email': 'wrongemail@none.co'}, 302)
    ])
    def test_should_return_ok(self, client, url, data, status_code):
        """
            Test que le code retourné est le bon selon le cas,
            nous vérifions ainsi le comportement de l'application, si l'email entré est valide ou s'il ne l'est pas
        """

        response = client.post(url, data=data)
        assert response.status_code == status_code
