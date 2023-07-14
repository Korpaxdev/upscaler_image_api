from dataclasses import dataclass
from os import getcwd
from pathlib import Path

APP_FOLDER = Path(getcwd())
TEMP_FOLDER = APP_FOLDER / "temp"
MODEL_PATH = APP_FOLDER / "upscaler/EDSR_x2.pb"
AVAILABLE_IMAGE_FORMAT = (".png", ".jpeg", ".jpg")

TEST_FILE_FOLDER = Path(getcwd()) / "tests/files"
DEFAULT_IMAGE = TEST_FILE_FOLDER / "picture.png"
TEMP_TEST_FOLDER = TEST_FILE_FOLDER / "temp"
BAD_FILE = TEST_FILE_FOLDER / "bad_file.txt"

TEST_DEFAULT_TIMEOUT_WAITING = 60


@dataclass(frozen=True)
class Errors:
    NEEDED_IMAGE = "Необходимо передать изображение в поле image"
    IMAGE_IS_PROCESSED = "Изображение с таким именем уже обрабатывается"
    FILE_NOT_FOUND = "Такой файл не найден"
    TASK_NOT_FOUND = "Такой задачи не существует, либо задача еще не была создана"
    INCORRECT_IMAGE_FORMAT = f"Неправильный формат изображения. Доступные форматы {', '.join(AVAILABLE_IMAGE_FORMAT)}"


@dataclass(frozen=True)
class TaskStatuses:
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CREATED = "CREATED"


@dataclass(frozen=True)
class InfoMessages:
    FILE_ALREADY_EXISTS = (
        "Файл с таким именем уже был загружен в базу. " "Upscale изображение вы сможете получить по ссылке ниже."
    )


MIMETYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
