import os
from pathlib import Path

from celery import Task, shared_task

from mongo.client import files_collection
from mongo.model import FileModel
from upscaler.upscale import upscale
from utils.path_utils import create_mimetype, get_file_name
from utils.variable_utils import TaskStatuses


@shared_task(bind=True)
def upscale_file(self: Task, file_path: str) -> str:
    self.update_state(state=TaskStatuses.CREATED)
    file_name = get_file_name(file_path)
    upscale(file_path, file_path)
    file_bytes = Path(file_path).read_bytes()
    file_model = FileModel(file=file_bytes, file_name=file_name, mimetype=create_mimetype(file_name))
    files_collection.insert_one(file_model.to_dict())
    background_remove.delay(file_path)
    return file_name


@shared_task
def background_remove(file_path: str) -> bool:
    try:
        os.remove(file_path)
    except Exception:
        return False
