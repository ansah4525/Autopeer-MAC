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
            # Split sentences on punctuation + space
            sentences = re.split(r'(?<=[.!?])\s+', para.strip())
            for sent in sentences:
                s = sent.strip()
                if not s:
                    continue

                words = s.split()
                if not words:
                    continue

                start_word = words[0].lower()
                end_word = words[-1].lower()

                # condition 1: starts with pronoun
                starts_with_pronoun = start_word in self.pronouns

                # condition 2: ends with pronoun
                ends_with_pronoun = end_word in self.pronouns

                # condition 3: comma before pronoun
                comma_pronoun = bool(
                    re.search(r",\s*(it|they|he|she|them|him|her|its)\b", s, flags=re.IGNORECASE)
                )

                if starts_with_pronoun or ends_with_pronoun or comma_pronoun:
                    issue_count += 1
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
