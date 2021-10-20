import unittest

import requests

from config import connection


class MyTestCase(unittest.TestCase):
    def test_get_pokemon_by_type(self):
        with connection.cursor()as cursor:
            query = 'insert into type (pokemon_id,pokemon_type) values(133,"normal")'
            cursor.execute(query)
            connection.commit()
        response = requests.get("http://127.0.0.1:3000/pokemon_by_type/normal")
        self.assertTrue('eevee' in response.json())
        new_response = requests.put("http://127.0.0.1:3000/updateTypes/eevee")
        if new_response.text[0:6] == 'Error:':
            print("cannot insert duplicate types")
        elif new_response.status_code == 500:
            print("internal error occurred")
        else:
            print("ok")


if __name__ == '__main__':
    unittest.main()
