from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from fastapi import Response
from app.main import app
from src.core import state


class Test_user_controller:

    def setup_method(self):
        self.client = TestClient(app)
        self.prefix = "/api/V1/users"

    def assign_globals(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        # Assign mock connection and cursor to global state
        state.conn = mock_conn
        state.cur = mock_cur
        state.logger = MagicMock()

    @patch("app.main.psycopg2.connect")
    def test_create_user_success(self, mock_connect):
        self.assign_globals(mock_connect)

        # params
        login = "testCrea03"
        name = "Broown"
        payload = {"login": login, "pwd": "testpwd", "nom": name}
        
        expected = {"message": "New user " + name + " created"}

        # call endpoint
        response = self.client.post(self.prefix + "/", json=payload)
        print("Response JSON:", response.json())

        # assertions
        assert response.status_code == 201
        assert response.json() == expected

    @patch("app.main.psycopg2.connect")
    def test_create_user_failure(self, mock_connect):
        self.assign_globals(mock_connect)
        #mock
        state.cur.execute.side_effect = Exception("DB insert failed")

        # params
        login = "testCrea03"
        name = "Broown"
        payload = {"login": login, "pwd": "testpwd", "nom": name}
        
        expected = {"message": "New user " + name + " created"}

        # call endpoint
        response = self.client.post(self.prefix + "/", json=payload)
        print("Response JSON:", response.json())

        # assertions
        assert response.status_code in (400, 500)

    @patch("app.main.psycopg2.connect")
    def test_create_user_invalid_inputs(self, mock_connect):
        self.assign_globals(mock_connect)

        # params
        login = "testCrea03"
        name = 33
        payload = {"login": login, "pwd": "testpwd", "nom": name}
        
        expected = {"detail": "Invalid input types"}

        # call endpoint
        response = self.client.post(self.prefix + "/", json=payload)
        print("Response JSON:", response.json())

        # assertions
        assert response.status_code == 422
        assert response.json() == expected

    @patch("app.main.psycopg2.connect")
    def test_list_users_with_results(self, mock_connect):
        self.assign_globals(mock_connect)
        #mock
        state.cur.fetchall.return_value = [("testCrea03", "Broown"), ("testCrea04", "Broown2")]
        state.cur.description = [
            ("login", None, None, None, None, None, None),
            ("name", None, None, None, None, None, None),
        ]
        
        expected = [{"login": "testCrea03", "name": "Broown"}, {"login": "testCrea04", "name": "Broown2"}]
        
        # call endpoint
        response = self.client.get(self.prefix + "/")
        print("Response JSON:", response.json())

        # assertions
        assert response.status_code == 200
        assert response.json() == expected        

    @patch("app.main.psycopg2.connect")
    def test_list_users_empty(self, mock_connect):
        self.assign_globals(mock_connect)
        #mock
        state.cur.fetchall.return_value = []
        state.cur.description = [
            ("login", None, None, None, None, None, None),
            ("name", None, None, None, None, None, None),
        ]
        
        expected = []
        
        # call endpoint
        response = self.client.get(self.prefix + "/")
        print("Response JSON:", response.json())

        # assertions
        assert response.status_code == 200
        assert response.json() == expected   

    @patch("app.main.psycopg2.connect")
    def test_list_users_failure(self, mock_connect):
        self.assign_globals(mock_connect)
        #mock
        state.cur.execute.side_effect = Exception("DB select failed")

        # call endpoint
        response = self.client.get(self.prefix + "/")
        print("Response JSON:", response.json())

        assert response.status_code == 400
