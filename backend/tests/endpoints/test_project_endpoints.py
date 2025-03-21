import unittest

from starlette import status
from starlette.testclient import TestClient

from app import app
from fill_database_mock import fill_database_mock
from tests.endpoints import assert_status_code, login_as, make_authenticated_request

# Define constants for URLs
GET_PROJECT_URL = "/api/projects/1"
GET_PROJECT_GROUPS_URL = "/api/projects/1/groups"
CREATE_GROUP_FOR_PROJECT_URL = "/api/projects/1/groups"
GET_PROJECT_STATISTICS = "/api/projects/1/statistics"
UPDATE_PROJECT_URL = "/api/projects/1"


class TestProjectEndpoints(unittest.TestCase):
    TESTED_USER_ID = 9  # Assuming the user ID is 9

    def setUp(self) -> None:
        self.client = TestClient(app)
        fill_database_mock()
        login_as(self.client, self.TESTED_USER_ID)

    def tearDown(self) -> None:
        pass

    def test_get_project(self) -> None:
        response = make_authenticated_request(self.client, self.TESTED_USER_ID, "get", GET_PROJECT_URL)
        assert_status_code(response, status.HTTP_200_OK)

    def test_get_project_groups(self) -> None:
        response = make_authenticated_request(self.client, self.TESTED_USER_ID, "get", GET_PROJECT_GROUPS_URL)
        assert_status_code(response, status.HTTP_200_OK)

    def test_create_group_for_project(self) -> None:
        response = make_authenticated_request(self.client, self.TESTED_USER_ID, "post", CREATE_GROUP_FOR_PROJECT_URL)
        assert_status_code(response, status.HTTP_200_OK)

    def test_get_project_statistics(self) -> None:
        response = make_authenticated_request(self.client, self.TESTED_USER_ID, "get", GET_PROJECT_STATISTICS)
        assert_status_code(response, status.HTTP_200_OK)
        res = response.json()
        self.assertTrue(res["submissions"] == res["approved"] + res["rejected"] + res["pending"])

    def test_update_project(self) -> None:
        project_data = {
            "name": "Updated Project",
            "deadline": "2024-12-31T23:59:59",
            "archived": False,
            "description": "Updated description",
            "requirements": '{"type":"SUBMISSION","root_constraint":{"type":"FILE","file_name":"submission.txt"},'
                            '"global_constraints":[]}',
            "visible": True,
            "max_students": 5,
            "dockerfile": "",
        }
        response = make_authenticated_request(
            self.client,
            self.TESTED_USER_ID,
            "put",
            UPDATE_PROJECT_URL,
            json=project_data,
        )
        assert_status_code(response, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
