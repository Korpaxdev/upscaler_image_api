from http import HTTPStatus

from flask import jsonify
from flask.views import MethodView

from celery_app.app import get_task
from utils.send_utils import send_error, send_task_success
from utils.url_utils import ex_url_for
from utils.variable_utils import Errors, TaskStatuses


class TaskView(MethodView):
    @staticmethod
    def get(task_id):
        task = get_task(task_id)

        if task.status == TaskStatuses.PENDING:
            return send_error(Errors.TASK_NOT_FOUND, HTTPStatus.NOT_FOUND)

        if task.status == TaskStatuses.SUCCESS:
            return send_task_success(task.status, ex_url_for("processed", file_name=task.result))

        return jsonify({"status": task.status})
