import os

from flask import Flask

from celery_app.app import make_celery
from utils.path_utils import create_path_if_not_exists
from utils.variable_utils import TEMP_FOLDER
from views.processed_view import ProcessedView
from views.task_view import TaskView
from views.upscale_view import UpscaleView
from dotenv import load_dotenv

load_dotenv()

celery_config = {
    "broker_url": os.getenv("CELERY_BROKER"),
    "result_backend": os.getenv("CELERY_BACKEND"),
    "broker_connection_retry_on_startup": True,
}

app = Flask(__name__)
app.config.from_mapping(CELERY=celery_config)

celery_app = make_celery(app)
create_path_if_not_exists(TEMP_FOLDER)

app.add_url_rule(rule="/upscale", view_func=UpscaleView.as_view("upscale"))
app.add_url_rule(rule="/tasks/<string:task_id>", view_func=TaskView.as_view("tasks"))
app.add_url_rule(rule="/processed/<path:file_name>", view_func=ProcessedView.as_view("processed"))
