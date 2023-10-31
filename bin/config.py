import sys
from cx_Freeze import setup, Executable

executables = [Executable("main.py", base=None)]
includes = [
    "cv2",
    "numpy",
    "mediapipe",
    "PIL",
    "time",
    "datetime",
    "pytz",
    "keras",
]
include_files = [
    ("model.keras"),  # Modelos Keras
]

options = {
    "build_exe": {
        "includes": includes,
        "include_files": include_files,
    },
}

setup(
    name="NomeDoSeuApp",
    version="1.0",
    description="Descrição do seu aplicativo",
    options=options,
    executables=executables,
)