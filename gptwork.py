
#this is a worker thread that calles openai 

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
                             QPushButton, QComboBox, QMessageBox, QAction, QMenu)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
from openai import OpenAI



class _GPTWorker(QThread):
    finished = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, prompt: str, model: str):
        super().__init__()
        self.prompt = prompt
        self.model = model

    def run(self):
        try:
            api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY is not set.")
            client = OpenAI(api_key=api_key)

            # Chat Completions API call (simple, reliable)
            # Docs: platform.openai.com/docs/api-reference/chat
            resp = client.chat.completions.create(
                model=self.model,  # e.g., "gpt-5" or "gpt-4.1"
                messages=[{"role": "user", "content": self.prompt}],
                temperature=1,
            )
            text = resp.choices[0].message.content or ""
            self.finished.emit(text.strip())
        except Exception as e:
            self.failed.emit(str(e))
