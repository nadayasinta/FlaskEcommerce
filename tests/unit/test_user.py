from blueprint.user.model import User
from blueprint.weather import PublicGetCurrentWeather
from blueprint import db
from mock import patch
from tests import reset_database

class TestUser():
    reset_database()

    def test_user_is_exsist(self):

        username = "unittesting2"

        assert User.is_exists(username) == True

class TestWeather():
    @patch.object(PublicGetCurrentWeather, 'get')
    def test_get_weather(self,mock_get):

        
        response = {
            "city": "Bandung",
            "organization": "AS9657 Melsa-i-net AS",
            "timezone": "Asia/Jakarta",
            "current_weather": {
                "date": "2019-09-04:07",
                "temp": 27.6
            }
        }

        mock_get.return_value = response

        assert PublicGetCurrentWeather.get('/weather?ip=202.138.233.162',) == response