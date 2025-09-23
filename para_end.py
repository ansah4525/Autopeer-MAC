import re
from typing import List, Dict

class ParagraphEndingChecker:
    def __init__(self):
        self.issue_counter = 0
        self.messages = []

        # Define word lists and patterns
        self.weak_conclusions = ["hence", "evidently"]
        self.repeated_conclusions = [
            "therefore", "thus", "as such", "as a result", "consequently", "accordingly"
        ]
        self.example_phrases = ["for example,", "for instance,"]
        self.reference_pattern = re.compile(r"\((\d{4}|n\.d\.)\)")
        self.quote_pattern = re.compile(r'"[^"]*"')

    def _extract_final_sentences(self, paragraphs: List[str]) -> List[str]:
        final_sentences = []
        for para in paragraphs:
            sentences = re.split(r'\.\s+', para.strip())
            if len(sentences) > 1:
                final_sentences.append(sentences[-1].strip())
            else:
                final_sentences.append("")  # Maintain paragraph index
        return final_sentences

    def analyze_text(self, text: str) -> Dict[str, str]:
        self.issue_counter = 0
        self.messages = []

        paragraphs = [p.strip() for p in text.strip().split("\n") if p.strip()]
        final_sentences = self._extract_final_sentences(paragraphs)
        total_paragraphs = len(paragraphs)

        last_conclusion_word = ""
        conclusion_words_found = False
        flagged_sentences = set()

        for i, (para, sentence) in enumerate(zip(paragraphs, final_sentences)):
            if len(re.split(r'\.\s+', para)) <= 1:
                continue  # skip single-sentence paragraphs

            lower_sentence = sentence.lower()

            if sentence in flagged_sentences:
                continue

            # Case 1: Weak conclusion words
            for wc in self.weak_conclusions:
                if lower_sentence.startswith(f"{wc},"):
                    self.issue_counter += 1
                    highlighted = sentence.replace(wc, f"<span style='color:red'>{wc}</span>")
                    self.messages.append(
                        f"<b>{i+1}.</b> {highlighted}<br>"
                        f"&nbsp;&nbsp;&nbsp;→ This sentence starts with '{wc},' which may sound dated or sarcastic.<br><br>"
                    )
                    flagged_sentences.add(sentence)
                    break

            # Case 2: Example phrases
            for phrase in self.example_phrases:
                if phrase in lower_sentence:
                    self.issue_counter += 1
                    highlighted = sentence.replace(phrase, f"<span style='color:red'>{phrase}</span>")
                    self.messages.append(
                        f"<b>{i+1}.</b> {highlighted}<br>"
                        f"&nbsp;&nbsp;&nbsp;→ Final sentence ends with an example. Consider adding elaboration.<br><br>"
                    )
                    flagged_sentences.add(sentence)
                    break

            # Case 3: Citation or quote
            if self.reference_pattern.search(sentence) or self.quote_pattern.search(sentence):
                self.issue_counter += 1
                self.messages.append(
                    f"<b>{i+1}.</b> {sentence}<br>"
                    f"&nbsp;&nbsp;&nbsp;→ Final sentence contains a citation or quote. Consider adding explanation.<br><br>"
                )
                flagged_sentences.add(sentence)

            # Case 4: Repeated conclusion words
            for word in self.repeated_conclusions:
                if lower_sentence.startswith(word):
                    if last_conclusion_word == word:
                        self.issue_counter += 1
                        highlighted = sentence.replace(word, f"<span style='color:red'>{word}</span>")
                        self.messages.append(
                            f"<b>{i+1}.</b> {highlighted}<br>"
                            f"&nbsp;&nbsp;&nbsp;→ Two consecutive paragraphs end with '{word}', which may feel repetitive.<br><br>"
                        )
                    last_conclusion_word = word
                    conclusion_words_found = True
                    break

        # Case 5: No conclusion words across 10+ paragraphs
        if total_paragraphs >= 10 and not conclusion_words_found:
            self.issue_counter += 1
            self.messages.append(
                "→ None of the final sentences in 10+ paragraph text begin with "
                "<span style='color:red'>therefore, thus, as such, as a result, consequently, or accordingly</span>.<br><br>"
            )

        if self.messages:
            return {
                "issues_found_counter": self.issue_counter,
                "issues_para": (
                    "<b>Auto-Peer: Paragraph Ending Issues</b><br><br>"
                    + "".join(self.messages)
                    + "Click ‘Explanations’ on the Auto-Peer menu if you need further information.<br><br>"
                ),
            }
        else:
            return {
                "issues_found_counter": 0,
                "issues_para": "No issues identified."
            }
