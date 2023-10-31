import sys
from cx_Freeze import setup, Executable

# Substitua 'seuarquivo.py' pelo nome do seu arquivo Python principal.
executables = [Executable("simultaneous_load.py", base=None)]

# Lista de bibliotecas que você deseja incluir no executável.
# Certifique-se de especificar todas as bibliotecas e módulos que seu projeto usa.
includes = [
    "cv2",
    "numpy",
    "mediapipe",
    "PIL",
    "time",
    "datetime",
    "pytz",
    "pandas",
    "keras",
    "pyautogui",
    "comtypes",
    "pycaw",
    "matplotlib",
]

# Diretórios e arquivos adicionais que você deseja incluir no executável.
# Certifique-se de ajustar os caminhos conforme necessário.
include_files = [
    ("../../models", "models"),  # Modelos Keras
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
