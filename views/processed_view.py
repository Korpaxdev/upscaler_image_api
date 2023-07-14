from http import HTTPStatus
from io import BytesIO

from flask import send_file
from flask.views import MethodView

from mongo.client import files_collection
from utils.send_utils import send_error
from utils.variable_utils import Errors


class ProcessedView(MethodView):
    @staticmethod
    def get(file_name):
        file_document = files_collection.find_one({"file_name": file_name})

        if file_document:
            file = file_document.get("file")
            mimetype = file_document.get("mimetype")
            return send_file(BytesIO(file), mimetype=mimetype)

        return send_error(Errors.FILE_NOT_FOUND, HTTPStatus.NOT_FOUND)
