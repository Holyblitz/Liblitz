from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from core.llm import ask_llm
from core.personality import PERSONALITY



BASE_DIR = Path(__file__).resolve().parent.parent
PORTRAIT_PATH = BASE_DIR / "assets" / "portraits" / "smile.png"


class LiblitzHome(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liblitz")
        self.resize(900, 700)

        self.portrait = QLabel()
        pixmap = QPixmap(str(PORTRAIT_PATH))
        self.portrait.setPixmap(
            pixmap.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.portrait.setAlignment(Qt.AlignCenter)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setPlaceholderText("Conversation avec Liblitz...")

        self.input = QLineEdit()
        self.input.setPlaceholderText("Écrire à Liblitz...")

        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_message)
        self.input.returnPressed.connect(self.send_message)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input)
        bottom_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.addWidget(self.portrait)
        layout.addWidget(self.chat)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
        self.apply_style()

    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0b16;
                color: #f5f0ff;
                font-family: "DejaVu Sans";
                font-size: 15px;
            }

            QTextEdit {
                background-color: #171022;
                border: 1px solid #4c1d95;
                border-radius: 12px;
                padding: 12px;
                color: #f5f0ff;
            }

            QLineEdit {
                background-color: #171022;
                border: 1px solid #6d28d9;
                border-radius: 10px;
                padding: 10px;
                color: #ffffff;
            }

            QPushButton {
                background-color: #6d28d9;
                color: white;
                border-radius: 10px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #7c3aed;
            }

            QPushButton:pressed {
                background-color: #5b21b6;
            }
        """)

    def set_portrait(self, image_name):
        path = BASE_DIR / "assets" / "portraits" / image_name

        pixmap = QPixmap(str(path))
        self.portrait.setPixmap(
            pixmap.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def choose_portrait(self, response):
        text = response.lower()

        if any(word in text for word in ["réfléch", "penser", "analyse", "regardons"]):
            return "thinking.png"

        if any(word in text for word in ["lis", "lecture", "document", "texte"]):
            return "analysis.png"

        if any(word in text for word in ["idée", "inspiration", "intuition"]):
            return "inspiration.png"

        if any(word in text for word in ["écoute", "comprends", "je vois"]):
            return "listening.png"

        if any(word in text for word in ["repos", "soir", "journée", "calme"]):
            return "evening.png"

        return "smile.png"

    def send_message(self):
        user_text = self.input.text().strip()

        if not user_text:
            return

        self.chat.append(f"<b>Romain :</b> {user_text}")
        self.input.clear()

        self.chat.append("<i>Liblitz réfléchit...</i>")
        self.set_portrait("thinking.png")
        QApplication.processEvents()

        prompt = f"""{PERSONALITY}

Conversation actuelle :

Romain : {user_text}

Liblitz :
"""

        response = ask_llm(prompt)

        portrait = self.choose_portrait(response)
        self.set_portrait(portrait)

        self.chat.append(f"<b>Liblitz :</b> {response}")
        self.chat.append("")
