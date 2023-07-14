import os
import time
import uuid
from http import HTTPStatus
from pathlib import Path
from shutil import rmtree

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from utils.variable_utils import BAD_FILE, DEFAULT_IMAGE, Errors, TaskStatuses, TEMP_TEST_FOLDER, \
    TEST_DEFAULT_TIMEOUT_WAITING

task_id_type = int | str

created_file: None | Path = None


class TestTasks:
    def test_not_found_task(self, client: FlaskClient):
        task_id = 1
        response = self.get_task(client, task_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json == self.error_response(Errors.TASK_NOT_FOUND)

    def test_task_without_file(self, client: FlaskClient):
        response = client.post("/upscale")
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == self.error_response(Errors.NEEDED_IMAGE)

    def test_task_with_bad_file(self, client: FlaskClient):
        response = client.post("/upscale", data={"image": BAD_FILE.open("rb")})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == self.error_response(Errors.INCORRECT_IMAGE_FORMAT)

    def test_with_new_file(self, client: FlaskClient):
        global created_file
        new_image_file = self.create_unique_image()
        created_file = new_image_file
        response = client.post("/upscale", data={"image": new_image_file.open("rb")})
        assert response.status_code == HTTPStatus.OK
        task_id = response.json.get("task_id")
        assert task_id
        created_task_response = self.wait_for_task_statuses(client, task_id, [TaskStatuses.CREATED])
        assert created_task_response.status_code == HTTPStatus.OK
        self.assert_status(created_task_response.json.get("status"), TaskStatuses.CREATED)
        completed_task_response = self.wait_for_task_statuses(
            client, task_id, [TaskStatuses.SUCCESS, TaskStatuses.FAILURE]
        )
        self.assert_status(completed_task_response.json.get("status"), TaskStatuses.SUCCESS)
        result_url = completed_task_response.json.get("url")
        assert result_url
        result_response = client.get(result_url)
        assert result_response.status_code == HTTPStatus.OK

    def test_with_file_in_db(self, client):
        try:
            global created_file
            response = client.post("/upscale", data={"image": created_file.open("rb")})
            assert response.status_code == HTTPStatus.OK
            url = response.json.get('url')
            assert url
            image_response = client.get(url)
            assert image_response.status_code == HTTPStatus.OK
        finally:
            rmtree(TEMP_TEST_FOLDER)

    def wait_for_task_statuses(
            self, client: FlaskClient, task_id: task_id_type, statuses: list[TaskStatuses],
            timeout=TEST_DEFAULT_TIMEOUT_WAITING
    ) -> TestResponse:
        response = self.get_task(client, task_id)
        timeout_count = 0

        while response.json.get("status") not in statuses:
            if timeout_count >= timeout:
                return response
            time.sleep(1)
            timeout_count += 1
            response = self.get_task(client, task_id)

        return response

    @staticmethod
    def get_task(client: FlaskClient, task_id: task_id_type) -> TestResponse:
        return client.get(f"/tasks/{task_id}")

    @staticmethod
    def assert_status(status: None | str, needed_status: TaskStatuses):
        assert status
        assert status == needed_status

    @staticmethod
    def error_response(message: Errors):
        return {"error": message}

    @staticmethod
    def create_unique_image() -> Path:
        image_bytes = DEFAULT_IMAGE.read_bytes()
        new_file_name = uuid.uuid4().hex + DEFAULT_IMAGE.suffix
        TEMP_TEST_FOLDER.mkdir(parents=True, exist_ok=True)
        new_path = TEMP_TEST_FOLDER / new_file_name
        with open(new_path, 'wb') as file:
            file.write(image_bytes)
        return new_path
