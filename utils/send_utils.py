from http import HTTPStatus

from flask import Response, jsonify

from utils.variable_utils import Errors, InfoMessages


def send_error(message: Errors, code: HTTPStatus = HTTPStatus.BAD_REQUEST) -> tuple[Response, int]:
    return jsonify({"error": message}), code


def send_info(message: InfoMessages, code: HTTPStatus = HTTPStatus.OK, additional: dict = None) -> tuple[Response, int]:
    info = {"info": message}
    if additional:
        info.update(additional)
    return jsonify(info), code


def send_task_info(task_id: int, task_process: str) -> Response:
    return jsonify({"task_id": task_id, "task_process": task_process})


def send_task_success(task_status: any, url: str) -> Response:
    return jsonify({"status": task_status, "url": url})
