import re
import spacy
from typing import Dict

class UnclearThisIssueChecker:
    def __init__(self):
        self.exceptions = {
            "study", "article", "method", "approach", "model", "paper", "research",
            "process", "finding", "analysis", "framework", "concept", "result",
            "idea", "theory", "section", "dataset", "issue", "evidence", "strategy",
            "paragraph", "investigation", "task", "application", "number"
        }
        self.this_counter = 0
        self.flagged = []
        self.nlp = spacy.load("en_core_web_sm")

    def _contains_adverb_after_this(self, sentence: str) -> bool:
        doc = self.nlp(sentence)
        for i, token in enumerate(doc):
            if token.lower_ == "this":
                if i + 1 < len(doc) and doc[i + 1].pos_ == "ADV":
                    return True
        return False

    def _flag_conditions(self, sentence: str):
        s = sentence.strip()
        lower = s.lower()
        doc = self.nlp(sentence)
        for i, token in enumerate(doc):
            if token.lower_ in {"this", "these"}:
                if i + 1 < len(doc) and doc[i + 1].pos_ in {"NOUN", "PROPN"}:
                    next_word = doc[i + 1].lemma_.lower()
                    if next_word in self.exceptions:
                        return (False, None)

        if len(s.split()) > 30 and re.search(r'\bthis\b', lower):
            return (True, "Very long sentence with 'this'")

        patterns = {
            r'\bthis\b[, ]+(shows|has|is|was|could|should|would|might|must|can|may|works|needs|demonstrates|suggests|displays|becomes|comes|means)': "Generic/weak verb after 'this'",
            r'\bthis\b[,]': "This followed by a comma",
            r'^[“"]?this\b': "Sentence starts with 'This'",
            r'; this\b': "This after semicolon",
            r'\bthis\b.+?(has|have|had) been': "This + passive verb ('been')",
            r'\bthis\b.+?(has|have|had) not': "This + negation",
            r'\bthis\b.+?(could|would|should|might|must) have': "This + modal verb ('could have', etc.)",
            r"\b(however|thus|therefore|moreover|furthermore|consequently|additionally|alternatively|nonetheless|nevertheless),\s*this\b": "Transition + 'this'",
            r'\bthis to\b': "This + 'to' (vague reference)",
            r'\bovercome these\b': "Vague 'these'",
            r'\blists these\b': "Lists + 'these'",
            r'\bthis\b not only\b': "This + 'not only'"
        }
        for pat, reason in patterns.items():
            if re.search(pat, lower):
                return (True, reason)

        if self._contains_adverb_after_this(sentence):
            return (True, "Adverb immediately after 'this'")

        match = re.search(r'\bthese\s+(\w+)', lower)
        if match:
            noun = match.group(1)
            if noun not in self.exceptions:
                return (True, f"Vague 'these' before '{noun}'")

        return (False, None)

    def analyze_text(self, text: str) -> Dict[str, str]:
        self.this_counter = 0
        self.flagged = []
        paragraphs = text.splitlines()

        for para in paragraphs:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for s in sentences:
                if "this" in s.lower() or "these" in s.lower():
                    should_flag, reason = self._flag_conditions(s)
                    if should_flag:
                        self.this_counter += 1
                        # Highlight pronoun(s) red
                        red_text = re.sub(
                            r'\b(this|these)\b',
                            r"<span style='color:red'>\1</span>",
                            s,
                            flags=re.IGNORECASE
                        )
                        # Bold the paragraph containing the flagged sentence
                        self.flagged.append(
                            f"{self.this_counter}. <b>{para}</b><br>   → {red_text}<br>   → Reason: {reason}"
                        )

        if self.flagged:
            return {
                "issues_found_counter": self.this_counter,
                "issues_para": (
                    "<b>Auto-Peer: Unclear #this/these# References</b><br><br>"
                    + "<br><br>".join(self.flagged)
                    + "<br><br>Click ‘Explanations’ on the Auto-Peer menu if you need further information."
                ),
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
