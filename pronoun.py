import re
import spacy
from typing import Dict, List
import en_core_web_sm

class PronounCohesionCheckerXojoExact:
    def __init__(self):
        self.pronouns = {"it", "they", "he", "she", "them", "him", "her", "its"}
        self.nlp = en_core_web_sm.load()

    def analyze_text(self, text: str) -> Dict[str, str]:
        paragraphs = text.strip().splitlines()
        flagged_sentences: List[str] = []
        issue_count = 0

        for para in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', para.strip())
            for sent in sentences:
                s = sent.strip()
                if not s:
                    continue

                # Check for start or end pronoun
                start_word = s.split()[0].lower() if s.split() else ""
                end_word = s.split()[-1].lower() if s.split() else ""
                comma_pronoun = bool(re.search(r",\s*(it|they|he|she|them|him|her)\b", s, flags=re.IGNORECASE))

                if start_word in self.pronouns or end_word in self.pronouns or comma_pronoun:
                    issue_count += 1
                    # Highlight pronouns in red
                    highlighted = re.sub(
                        r'\b(it|they|them|he|she|him|her|its)\b',
                        r"<span style='color:red'>\1</span>",
                        s,
                        flags=re.IGNORECASE
                    )
                    flagged_sentences.append(f"{issue_count}. <b>{highlighted}</b>")

        if flagged_sentences:
            return {
                "issues_found_counter": issue_count,
                "issues_para": (
                    "<b>Pronoun Cohesion – Flagged Sentences</b><br><br>"
                    + "<br><br>".join(flagged_sentences)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
