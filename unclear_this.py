import re
import spacy
from typing import Dict, List

class UnclearThisIssueChecker:
    def __init__(self, exceptions_file: str = "exceptions.txt"):
        # Load exceptions from file into a set
        self.exceptions = self._load_exceptions(exceptions_file)
        self.this_counter = 0
        self.flagged: List[str] = []
        self.nlp = spacy.load("en_core_web_sm")

    def _load_exceptions(self, filepath: str) -> set:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                # strip each line and ignore empties
                return {line.strip().lower() for line in f if line.strip()}
        except FileNotFoundError:
            print(f"[Warning] Exception file '{filepath}' not found. Using empty list.")
            return set()

    def _flag_conditions(self, sentence: str) -> bool:
        """
        Only flag if 'this' or 'these' is followed by a word:
        - ≥5 letters
        - ends with 's'
        - not in exceptions
        """
        doc = self.nlp(sentence)
        for i, token in enumerate(doc):
            if token.lower_ in {"this"}:
                if i + 1 < len(doc):
                    next_word = doc[i + 1].text.lower()
                    if (
                        len(next_word) >= 5
                        and next_word.endswith("s")
                        and next_word not in self.exceptions
                    ):
                        return True
        return False

    def analyze_text(self, text: str) -> Dict[str, str]:
        self.this_counter = 0
        self.flagged = []
        paragraphs = text.splitlines()

        for para in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for s in sentences:
                if "this" in s.lower() or "these" in s.lower():
                    if self._flag_conditions(s):
                        self.this_counter += 1
                        # highlight the this/these red
                        red_text = re.sub(
                            r'\b(this|these)\b',
                            r"<span style='color:red'>\1</span>",
                            s,
                            flags=re.IGNORECASE
                        )
                        # add numbered, bold sentence only
                        self.flagged.append(f"{self.this_counter}. <b>{red_text}</b>")

        if self.flagged:
            return {
                "issues_found_counter": self.this_counter,
                "issues_para": (
                    "<b>Auto-Peer: Unclear this References</b><br><br>"
                    + "<br><br>".join(self.flagged)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                ),
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
