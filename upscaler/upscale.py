import cv2
from cv2 import dnn_superres

from utils.variable_utils import MODEL_PATH

scaler = dnn_superres.DnnSuperResImpl_create()
scaler.readModel(str(MODEL_PATH))
scaler.setModel("edsr", 4)


def upscale(input_path: str, output_path: str) -> None:
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)
