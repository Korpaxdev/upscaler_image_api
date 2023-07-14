from os import path
from pathlib import Path

from utils.variable_utils import AVAILABLE_IMAGE_FORMAT, MIMETYPES, TEMP_FOLDER


def create_path_if_not_exists(file_path: Path) -> None:
    file_path.mkdir(parents=True, exist_ok=True)


def get_file_name(file_path: Path | str) -> str:
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.name


def is_image(file_name: str) -> bool:
    file_name = Path(file_name)
    return file_name.suffix in AVAILABLE_IMAGE_FORMAT


def get_uploaded_path(file_name: str) -> Path:
    return TEMP_FOLDER / file_name


def path_exists(file_path: Path) -> bool:
    return path.exists(file_path)


def create_mimetype(file_name: str):
    file_ext = Path(file_name).suffix
    mimetype = MIMETYPES.get(file_ext, MIMETYPES[".jpg"])
    return mimetype
