from flask import request
from flask.views import MethodView

from celery_app.tasks import upscale_file
from mongo.client import files_collection
from utils.path_utils import get_file_name, get_uploaded_path, is_image, path_exists
from utils.send_utils import send_error, send_info, send_task_info
from utils.url_utils import ex_url_for
from utils.variable_utils import Errors, InfoMessages


class UpscaleView(MethodView):
    @staticmethod
    def post():
        if not request.files or not request.files.get("image"):
            return send_error(Errors.NEEDED_IMAGE)

        image = request.files["image"]
        file_name = get_file_name(image.filename)

        if not is_image(file_name):
            return send_error(Errors.INCORRECT_IMAGE_FORMAT)

        if files_collection.find_one({"file_name": file_name}):
            return send_info(
                InfoMessages.FILE_ALREADY_EXISTS, additional={"url": ex_url_for("processed", file_name=file_name)}
            )

        uploaded_path = get_uploaded_path(file_name)

        if path_exists(uploaded_path):
            return send_error(Errors.IMAGE_IS_PROCESSED)
        image.save(uploaded_path)
        async_result = upscale_file.delay(str(uploaded_path))
        task_id = async_result.id
        task_process_url = ex_url_for("tasks", task_id=task_id)
        return send_task_info(task_id, task_process_url)
