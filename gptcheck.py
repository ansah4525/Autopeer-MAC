
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
                             QPushButton, QComboBox, QMessageBox, QAction, QMenu)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
from openai import OpenAI

from gptwork import _GPTWorker
class GPTChatDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GPT Chat")
        self.setMinimumSize(720, 540)

        layout = QVBoxLayout(self)

        # Model picker
        top = QHBoxLayout()
        top.addWidget(QLabel("Model:"))
        self.model_box = QComboBox()
        # Offer a couple of good defaults; you can add/rename as you wish
        self.model_box.addItems(["gpt-5", "gpt-4.1", "gpt-3.5","gpt-4o-mini"])
        top.addWidget(self.model_box)
        top.addStretch(1)
        layout.addLayout(top)

        # Prompt editor
        layout.addWidget(QLabel("Prompt:"))
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlaceholderText("Type your prompt…")
        layout.addWidget(self.prompt_edit, 2)

        # Buttons
        btns = QHBoxLayout()
        self.send_btn = QPushButton("Send")
        self.clear_btn = QPushButton("Clear")
        btns.addStretch(1)
        btns.addWidget(self.clear_btn)
        btns.addWidget(self.send_btn)
        layout.addLayout(btns)

        # Output
        layout.addWidget(QLabel("Response:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output, 3)

        # Wire up
        self.send_btn.clicked.connect(self._on_send)
        self.clear_btn.clicked.connect(self._on_clear)

        self.worker = None

    def _on_clear(self):
        self.prompt_edit.clear()
        self.output.clear()

    def _on_send(self):
        prompt = self.prompt_edit.toPlainText().strip()
        if not prompt:
            QMessageBox.information(self, "GPT Chat", "Please enter a prompt.")
            return

        model = self.model_box.currentText()
        self._set_busy(True)
        self.output.append("→ Sending…")

        self.worker = _GPTWorker(prompt, model)
        self.worker.finished.connect(self._on_result)
        self.worker.failed.connect(self._on_error)
        self.worker.start()

    def _on_result(self, text: str):
        self._set_busy(False)
        self.output.append("\n← Response:\n" + text + "\n")

    def _on_error(self, msg: str):
        self._set_busy(False)
        QMessageBox.critical(self, "OpenAI error", msg)

    def _set_busy(self, busy: bool):
        self.send_btn.setEnabled(not busy)
        self.clear_btn.setEnabled(not busy)
        self.prompt_edit.setReadOnly(busy)
