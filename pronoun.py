import re
import spacy
from typing import Dict, List
import en_core_web_sm

class PronounCohesionCheckerXojoExact:
    def __init__(self):
        self.start_pronouns = {"it", "they", "he", "she", "its"}
        self.end_pronouns = {"it", "them", "him", "her"}
        self.transition_words = {
            "however", "therefore", "thus", "moreover", "furthermore", "consequently",
            "additionally", "alternatively", "nonetheless", "nevertheless"
        }
        self.copular_verbs = {"be", "is", "was", "are", "were", "been", "being"}
        
        self.nlp = en_core_web_sm.load()


    # ---- reason detectors ----
    def _reason_copular(self, doc) -> bool:
        for token in doc:
            if token.lower_ in self.start_pronouns and token.dep_ in {"nsubj", "nsubjpass"}:
                if token.head.lemma_ in self.copular_verbs:
                    return True
        return False

    def _reason_transition_then_pronoun(self, doc) -> bool:
        if len(doc) >= 2 and doc[0].lower_ in self.transition_words and doc[1].lower_ in self.start_pronouns:
            return True
        if len(doc) >= 3 and doc[0].lower_ in self.transition_words and doc[1].text == "," and doc[2].lower_ in self.start_pronouns:
            return True
        return False

    def _reason_main_clause_pronoun(self, doc) -> bool:
        root = next((t for t in doc if t.dep_ == "ROOT"), None)
        if not root:
            return False
        for token in doc:
            if token.lower_ in self.start_pronouns and token.head == root and token.dep_ in {"nsubj", "nsubjpass"}:
                return True
        return False

    def _reason_comma_before_pronoun(self, text: str) -> bool:
        return bool(re.search(r",\s*(it|they|he|she)\b", text, flags=re.IGNORECASE))

    def _reason_long_with_pronoun(self, text: str) -> bool:
        return len(text.split()) > 20 and re.search(r"\b(it|they|them|he|she|him|her)\b", text, re.IGNORECASE)

    # ---- main ----
    def analyze_text(self, text: str) -> Dict[str, str]:
        paragraphs = text.strip().splitlines()
        flagged_lines: List[str] = []
        issue_count = 0

        for para in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', para.strip())
            for sent in sentences:
                s = sent.strip()
                if not s:
                    continue

                doc = self.nlp(s)
                reasons = []

                if self._reason_main_clause_pronoun(doc):
                    reasons.append("Pronoun as main-clause subject")
                if self._reason_transition_then_pronoun(doc):
                    reasons.append("Starts with transition + pronoun")
                if self._reason_copular(doc):
                    reasons.append("Copular construction (e.g., “It is …”)")
                if self._reason_comma_before_pronoun(s):
                    reasons.append("Comma directly before pronoun")
                if self._reason_long_with_pronoun(s):
                    reasons.append("Very long sentence with pronoun")

                if reasons:
                    issue_count += 1
                    # highlight pronouns red
                    highlighted = re.sub(
                        r'\b(it|they|them|he|she|him|her|its)\b',
                        r"<span style='color:red'>\1</span>",
                        s,
                        flags=re.IGNORECASE
                    )
                    # format with line breaks
                    reason_text = "<br>   → " + "<br>   → ".join(reasons)
                    flagged_lines.append(f"{issue_count}. {highlighted}<br>{reason_text}")

        if flagged_lines:
            return {
                "issues_found_counter": issue_count,
                "issues_para": (
                    "<b>^Pronoun Cohesion^</b><br><br>"
                    + "<br><br>".join(flagged_lines)
                    + "<br><br>The sentences above include pronouns like 'it', 'they', 'he', or 'she' "
                      "in positions that can weaken cohesion. Consider naming the referent explicitly.<br>"
                      "Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                )
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
